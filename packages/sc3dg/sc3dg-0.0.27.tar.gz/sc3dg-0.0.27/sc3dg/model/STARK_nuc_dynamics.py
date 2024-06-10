# Python functions for NucDynamics
import sys
import numpy as np
import multiprocessing
from multiprocessing import Queue, Process
from time import time
import os
import gzip
from sc3dg.model import STARK_dyn_3dg as dyn_3dg

PROG_NAME = 'nuc_dynamics'
DESCRIPTION = 'Single-cell Hi-C genome and chromosome structure calculation module for 3DG'

N3D = 'n3d'
PDB = 'pdb'
FORMATS = [N3D, PDB]
MAX_CORES = multiprocessing.cpu_count()

def warn(msg, prefix='WARNING'):

  print('%8s : %s' % (prefix, msg))


def critical(msg, prefix='ABORT'):

  print('%8s : %s' % (prefix, msg))
  sys.exit(0)
  
  
def _parallel_func_wrapper(queue, target_func, proc_data, common_args):
  
  for t, data_item in proc_data:
    result = target_func(data_item, *common_args)
    
    if queue:
      queue.put((t, result))
    
    elif isinstance(result, Exception):
      raise(result)


def parallel_split_job(target_func, split_data, common_args, num_cpu=MAX_CORES, collect_output=True):
  num_tasks = len(split_data)
  num_process = min(num_cpu, num_tasks)

  processes = []
  queue = Queue() if collect_output else None

  for p in range(num_process):
    proc_data = [(t, data_item) for t, data_item in enumerate(split_data) if t % num_process == p]
    args = (queue, target_func, proc_data, common_args)
    proc = Process(target=_parallel_func_wrapper, args=args)
    processes.append(proc)

  for proc in processes:
    proc.start()

  if collect_output:
    results = [None] * num_tasks
    for _ in range(num_tasks):
      t, result = queue.get()
      if isinstance(result, Exception):
        print('\n* * * * C/Cython code may need to be recompiled. Try running "python setup_cython.py build_ext --inplace" * * * *\n')
        raise result
      results[t] = result
    queue.close()
    queue.join_thread()
    return results
  else:
    for proc in processes:
      proc.join()


def load_pair_file(file_path, target_Chrom):
  """Load chromosome and contact data from NCC format file, as output from NucProcess"""
  
  if file_path.endswith('.gz'):
    import gzip
    file_obj = gzip.open(file_path,'rb')
  
  else:
    file_obj = open(file_path) 
  
  # Observations are treated individually in single-cell Hi-C,
  # i.e. no binning, so num_obs always 1 for each contact
  num_obs = 1  
    
  contact_dict = {}
  chromosomes = set()
    
  for line in file_obj:
    line = line.decode()
    if "#" == line[0]:
      continue
    #chr_a, f_start_a, f_end_a, start_a, end_a, strand_a, chr_b, f_start_b, f_end_b, start_b, end_b, strand_b, ambig_group, pair_id, swap_pair = line.split()
    # print(line.split('\t'))
    PairId, chr_a, f_start_a, chr_b, f_start_b, strand_a, strand_b, pairType, mapq1, mapq2 = line.split("\t")[0:10]

    if chr_a =="!" or chr_b =="!" or pairType != "UU":
      continue

    if chr_a not in target_Chrom or chr_b not in target_Chrom:
      continue

    pos_a = int(f_start_a)
    pos_b = int(f_start_b)
 
    if chr_a > chr_b:
      chr_a, chr_b = chr_b, chr_a
      pos_a, pos_b = pos_b, pos_a
    
    if chr_a not in contact_dict:
      contact_dict[chr_a] = {}
      chromosomes.add(chr_a)
      
    if chr_b not in contact_dict[chr_a]:
      contact_dict[chr_a][chr_b] = [] 
      chromosomes.add(chr_b)
        
    contact_dict[chr_a][chr_b].append((pos_a, pos_b, num_obs, int(1)))
   
  file_obj.close()

  contact_dict = {key: contact_dict[key] for key in sorted(contact_dict.keys())}
  chromo_limits = {}
    
  for chr_a in contact_dict:
    for chr_b in contact_dict[chr_a]:
      contacts = np.array(contact_dict[chr_a][chr_b]).T
      contact_dict[chr_a][chr_b] = contacts
      
      seq_pos_a = contacts[0]
      seq_pos_b = contacts[1]
      
      min_a = min(seq_pos_a)
      max_a = max(seq_pos_a)
      min_b = min(seq_pos_b)
      max_b = max(seq_pos_b)
        
      if chr_a in chromo_limits:
        prev_min, prev_max = chromo_limits[chr_a]
        chromo_limits[chr_a] = [min(prev_min, min_a), max(prev_max, max_a)]
      else:
        chromo_limits[chr_a] = [min_a, max_a]
      
      if chr_b in chromo_limits:
        prev_min, prev_max = chromo_limits[chr_b]
        chromo_limits[chr_b] = [min(prev_min, min_b), max(prev_max, max_b)]
      else:
        chromo_limits[chr_b] = [min_b, max_b]
         
  chromosomes = sorted(chromosomes)      
        
  return chromosomes, chromo_limits, contact_dict


def export_n3d_coords(file_path, coords_dict, seq_pos_dict):
  
  file_obj = open(file_path, 'w')
  write = file_obj.write
  
  for chromo in seq_pos_dict:
    chromo_coords = coords_dict[chromo]
    chromo_seq_pos = seq_pos_dict[chromo]
    
    num_models = len(chromo_coords)
    num_coords = len(chromo_seq_pos)
    
    line = '%s\t%d\t%d\n' % (chromo, num_coords, num_models)
    write(line)
    
    for j in range(num_coords):
      data = chromo_coords[:,j].ravel().tolist()
      data = '\t'.join('%.8f' % d for d in  data)
      
      line = '%d\t%s\n' % (chromo_seq_pos[j], data)
      write(line)

  file_obj.close()


def export_pdb_coords(file_path, coords_dict, seq_pos_dict, particle_size, scale=1.0, extended=True):
  """
  Write chromosome particle coordinates as a PDB format file
  """

  alc = ' '
  ins = ' '
  prefix = 'HETATM'
  line_format = '%-80.80s\n'
  
  if extended:
    pdb_format = '%-6.6s%5.1d %4.4s%s%3.3s %s%4.1d%s   %8.3f%8.3f%8.3f%6.2f%6.2f          %2.2s  %10d\n'
    ter_format = '%-6.6s%5.1d      %s %s%4.1d%s                                                     %10d\n'
  else:
    pdb_format = '%-6.6s%5.1d %4.4s%s%3.3s %s%4.1d%s   %8.3f%8.3f%8.3f%6.2f%6.2f          %2.2s  \n'
    ter_format = '%-6.6s%5.1d      %s %s%4.1d%s                                                     \n'

  file_obj = open(file_path, 'w')
  write = file_obj.write
  
  chromosomes = list(seq_pos_dict.keys())
  
  sort_chromos = []
  for chromo in chromosomes:
    if chromo[:3] == 'chr':
      key = chromo[3:]
    else:
      key = chromo
    
    if key.isdigit():
      key = '%03d' % int(key)
    
    sort_chromos.append((key, chromo))
  
  sort_chromos.sort()
  sort_chromos = [x[1] for x in sort_chromos]
  
  num_models = len(coords_dict[chromosomes[0]])
  title = 'NucDynamics genome structure export'
  
  write(line_format % 'TITLE     %s' % title)
  write(line_format % 'REMARK 210') 
  write(line_format % 'REMARK 210 Atom type C is used for all particles')
  write(line_format % 'REMARK 210 Atom number increases every %s bases' % particle_size)
  write(line_format % 'REMARK 210 Residue code indicates chromosome')
  write(line_format % 'REMARK 210 Residue number represents which sequence Mb the atom is in')
  write(line_format % 'REMARK 210 Chain letter is different every chromosome, where Chr1=a, Chr2=b etc.')
  
  if extended:
    file_obj.write(line_format % 'REMARK 210 Extended PDB format with particle seq. pos. in last column')
  
  file_obj.write(line_format % 'REMARK 210')
  
  pos_chromo = {}
  
  for m in range(num_models):
    line = 'MODEL     %4d' % (m+1)
    write(line_format  % line)
    
    c = 0
    j = 1
    seqPrev = None
    
    for k, chromo in enumerate(sort_chromos):
      chain_code = chr(ord('a')+k)            
      
      tlc = chromo
      while len(tlc) < 2:
        tlc = '_' + tlc
      
      if len(tlc) == 2:
        tlc = 'C' + tlc
      
      if len(tlc) > 3:
        tlc = tlc[:3]
      
      chromo_model_coords = coords_dict[chromo][m]
      
      if not len(chromo_model_coords):
        continue
      
      pos = seq_pos_dict[chromo]
      
      for i, seqPos in enumerate(pos):
        c += 1
 
        seqMb = int(seqPos//1e6) + 1
        
        if seqMb == seqPrev:
          j += 1
        else:
          j = 1
        
        el = 'C'
        a = 'C%d' % j
          
        aName = '%-3s' % a
        x, y, z = chromo_model_coords[i] #XYZ coordinates
         
        seqPrev = seqMb
        pos_chromo[c] = chromo
        
        if extended:
          line  = pdb_format % (prefix,c,aName,alc,tlc,chain_code,seqMb,ins,x,y,z,0.0,0.0,el,seqPos)
        else:
          line  = pdb_format % (prefix,c,aName,alc,tlc,chain_code,seqMb,ins,x,y,z,0.0,0.0,el)
          
        write(line)
 
    write(line_format  % 'ENDMDL')
 
  for i in range(c-2):
     if pos_chromo[i+1] == pos_chromo[i+2]:
       line = 'CONECT%5.1d%5.1d' % (i+1, i+2)
       write(line_format  % line)
 
  write(line_format  % 'END')
  file_obj.close()


def remove_isolated_contacts(contact_dict, threshold=int(2e6)):
  """
  Select only contacts which are within a given sequence separation of another
  contact, for the same chromosome pair
  """
    
  for chromoA in contact_dict:
    print(chromoA)
    for chromoB in contact_dict[chromoA]:
      contacts = contact_dict[chromoA][chromoB]
      positions = np.array(contacts[:2], np.int32).T
      
      if len(positions): # Sometimes empty e.g. for MT, Y chromos 
        active_idx = dyn_3dg.getSupportedPairs(positions, np.int32(threshold))
        contact_dict[chromoA][chromoB] = contacts[:,active_idx]
     
  return contact_dict
  

def remove_violated_contacts(contact_dict, coords_dict, particle_seq_pos, particle_size, threshold=5.0):  
  """
  Remove contacts whith structure distances that exceed a given threshold
  """
  
  for chr_a in contact_dict:
    for chr_b in contact_dict[chr_a]:
      contacts = contact_dict[chr_a][chr_b]
      
      contact_pos_a = contacts[0].astype(np.int32)
      contact_pos_b = contacts[1].astype(np.int32)
      
      coords_a = coords_dict[chr_a]
      coords_b = coords_dict[chr_b]

      struc_dists = []
 
      for m in range(len(coords_a)):
        coord_data_a = dyn_3dg.getInterpolatedCoords([chr_a], {chr_a:contact_pos_a}, particle_seq_pos, coords_a[m])
        coord_data_b = dyn_3dg.getInterpolatedCoords([chr_b], {chr_b:contact_pos_b}, particle_seq_pos, coords_b[m])
 
        deltas = coord_data_a - coord_data_b
        dists = np.sqrt((deltas*deltas).sum(axis=1))
        struc_dists.append(dists)
      
      # Average over all conformational models
      struc_dists = np.array(struc_dists).T.mean(axis=1)
      
      # Select contacts with distances below distance threshold
      indices = (struc_dists < threshold).nonzero()[0]
      contact_dict[chr_a][chr_b] = contacts[:,indices]
        
  return contact_dict
  
  
def get_random_coords(pos_dict, chromosomes, num_models, radius=10.0):
  """
  Get random, uniformly sampled coorinate positions, restricted to
  a sphere of given radius
  """
    
  from numpy.random import uniform
    
  num_particles = sum([len(pos_dict[chromo]) for chromo in chromosomes])
  coords = np.empty((num_models, num_particles, 3))
  r2 = radius*radius
    
  for m in range(num_models):
    
    for i in range(num_particles):
      x = y = z = radius

      while x*x + y*y + z*z >= r2:
        x = radius * (2*uniform(0,1) - 1)
        y = radius * (2*uniform(0,1) - 1)
        z = radius * (2*uniform(0,1) - 1)
      
      coords[m,i] = [x,y,z]

  return coords
  
  
def pack_chromo_coords(coords_dict, chromosomes):
  """
  Place chromosome 3D coordinates stored in a dictionary keyed by
  chromosome name into a single, ordered array. The chromosomes argument
  is required to set the correct array storage order.
  """

  chromo_num_particles = [len(coords_dict[chromo][0]) for chromo in chromosomes]
  n_particles = sum(chromo_num_particles)
  n_models = len(coords_dict[chromosomes[0]])  
  coords = np.empty((n_models, n_particles, 3), float)
  
  j = 0
  for i, chromo in enumerate(chromosomes):
    span = chromo_num_particles[i]
    coords[:,j:j+span] = coords_dict[chromo]
    j += span
      
  return coords
  
 
def unpack_chromo_coords(coords, chromosomes, seq_pos_dict):
  """
  Exctract coords for multiple chromosomes stored in a single array into
  a dictionary, keyed by chromosome name. The chromosomes argument is required
  to get the correct array storage order.
  """

  chromo_num_particles = [len(seq_pos_dict[chromo]) for chromo in chromosomes]
  n_seq_pos = sum(chromo_num_particles)
  n_models, n_particles, dims = coords.shape

  if n_seq_pos != n_particles:
    msg = 'Model coordinates must be an array of num models x %d' % (n_seq_pos,)
    raise(Exception(msg))  
  
  coords_dict = {}
        
  j = 0
  for i, chromo in enumerate(chromosomes):
    span = chromo_num_particles[i]
    coords_dict[chromo] = coords[:,j:j+span] # all models, slice
    j += span
 
  return coords_dict


def anneal_model(model_data, anneal_schedule, masses, radii, restraint_indices, restraint_dists,
                 ambiguity, temp, time_step, dyn_steps, repulse, n_rep_max):

  import gc
  
  m, model_coords = model_data
  
  # Anneal one model in parallel
  
  time_taken = 0.0
  
  if m == 0:
    printInterval = max(1, dyn_steps/2)
  
  else:
    printInterval = 0
  
  print('  starting model %d' % m)
  
  for temp, repulse in anneal_schedule:
    gc.collect() # Try to free some memory
    
    # Update coordinates for this temp
    
    try:  
      dt, n_rep_max = dyn_3dg.runDynamics(model_coords, masses, radii, restraint_indices, restraint_dists,
                                           ambiguity, temp, time_step, dyn_steps, repulse, nRepMax=n_rep_max,
                                           printInterval=printInterval)
    
    except Exception as err:
      return err
 
    n_rep_max = np.int32(1.05 * n_rep_max) # Base on num in prev cycle, plus a small overhead
    time_taken += dt
  
  # Center
  model_coords -= model_coords.mean(axis=0)

  print('  done model %d' % m)
  
  return model_coords
 
  
def anneal_genome(chromosomes, contact_dict, num_models, particle_size,
                  general_calc_params, anneal_params,
                  prev_seq_pos_dict=None, start_coords=None, num_cpu=MAX_CORES):
    """
    Use chromosome contact data to generate distance restraints and then
    apply a simulated annealing protocul to generate/refine coordinates.
    Starting coordinates may be random of from a previous (e.g. lower
    resolution) stage.
    """
    
    from numpy import random
    from math import log, exp, atan, pi
    
    random.seed(general_calc_params['random_seed'])
    particle_size = np.int32(particle_size)
    
    # Calculate distance restrains from contact data   
    restraint_dict, seq_pos_dict = dyn_3dg.calc_restraints(chromosomes, contact_dict, particle_size,
                                                   scale=1.0, exponent=general_calc_params['dist_power_law'],
                                                   lower=general_calc_params['contact_dist_lower'],
                                                   upper=general_calc_params['contact_dist_upper'])
    
    # Concatenate chromosomal data into a single array of particle restraints
    # for structure calculation. Add backbone restraints between seq. adjasent particles.
    restraint_indices, restraint_dists = dyn_3dg.concatenate_restraints(restraint_dict, seq_pos_dict, particle_size,
                                                                general_calc_params['backbone_dist_lower'],
                                                                general_calc_params['backbone_dist_upper'])
 
    # Setup starting structure
    if (start_coords is None) or (prev_seq_pos_dict is None):
      coords = get_random_coords(seq_pos_dict, chromosomes, num_models,
                                 general_calc_params['random_radius'])
      
      num_coords = coords.shape[1]
            
    else:
      # Convert starting coord dict into single array
      coords = pack_chromo_coords(start_coords, chromosomes)
      num_coords = sum([len(seq_pos_dict[c]) for c in chromosomes])
        
      if coords.shape[1] != num_coords: # Change of particle_size
        interp_coords = np.empty((num_models, num_coords, 3))
        
        for m in range(num_models): # Starting coords interpolated from previous particle positions
          interp_coords[m] = dyn_3dg.getInterpolatedCoords(chromosomes, seq_pos_dict, prev_seq_pos_dict, coords[m])
        
        coords = interp_coords
        
    # Equal unit masses and radii for all particles
    masses = np.ones(num_coords,  float)
    radii = np.ones(num_coords,  float)
    
    # Ambiguiity strides not used here, so set to 1
    num_restraints = len(restraint_indices)
    ambiguity = np.ones(num_restraints,  np.int32)
        
    # Below will be set to restrict memory allocation in the repusion list
    # (otherwise all vs all can be huge)
    n_rep_max = np.int32(0)
    
    # Annealing parameters
    temp_start = anneal_params['temp_start']
    temp_end = anneal_params['temp_end']
    temp_steps = anneal_params['temp_steps']
    
    # Setup annealig schedule: setup temps and repulsive terms
    adj = 1.0 / atan(10.0)
    decay = log(temp_start/temp_end)    
    anneal_schedule = []
    
    for step in range(temp_steps):
      frac = step/float(temp_steps)
    
      # exponential temp decay
      temp = temp_start * exp(-decay*frac)
    
      # sigmoidal repusion scheme
      repulse = 0.5 + adj * atan(frac*20.0-10) / pi 
      
      anneal_schedule.append((temp, repulse))  
        
    # Paricle dynamics parameters
    # (these need not be fixed for all stages, but are for simplicity)    
    dyn_steps = anneal_params['dynamics_steps']
    time_step = anneal_params['time_step']
       
    # Update coordinates in the annealing schedule which is applied to each model in parallel
    common_args = [anneal_schedule, masses, radii, restraint_indices, restraint_dists,
                   ambiguity, temp, time_step, dyn_steps, repulse, n_rep_max]
    
    task_data = [(m, coords[m]) for m in range(len(coords))]

    coords = parallel_split_job(anneal_model, task_data, common_args, int(num_cpu), collect_output=True)
    coords = np.array(coords)
   
    # Convert from single coord array to dict keyed by chromosome
    coords_dict = unpack_chromo_coords(coords, chromosomes, seq_pos_dict)
    
    return coords_dict, seq_pos_dict


def open_file(file_path, mode=None, gzip_exts=('.gz','.gzip')):
  """
  GZIP agnostic file opening
  """
  IO_BUFFER = int(4e6)
  
  if os.path.splitext(file_path)[1].lower() in gzip_exts:
    file_obj = gzip.open(file_path, mode or 'rt')
  else:
    file_obj = open(file_path, mode or 'rU', IO_BUFFER)
 
  return file_obj

def load_n3d_coords(file_path):
 """
 Load genome structure coordinates and particle sequence positions from an N3D format file.

 Args:
     file_path: str ; Location of N3D (text) format file

 Returns:
     dict {str:ndarray(n_coords, int)}                  ; {chromo: seq_pos_array}
     dict {str:ndarray((n_models, n_coords, 3), float)} ; {chromo: coord_3d_array}

 """
 seq_pos_dict = {}
 coords_dict = {}

 with open_file(file_path) as file_obj:
   chromo = None

   for line in file_obj:

     data = line.split()
     n_items = len(data)

     if not n_items:
       continue

     elif data[0] == '#':
       continue

     elif n_items == 3:
       chromo, n_coords, n_models = data

       #if chromo.lower()[:3] == 'chr':
       #  chromo = chromo[3:]

       n_coords = int(n_coords)
       n_models = int(n_models)

       #chromo_seq_pos = np.empty(n_coords, int)
       chromo_seq_pos = np.empty(n_coords, 'int32')
       chromo_coords = np.empty((n_models, n_coords, 3), float)

       coords_dict[chromo]  = chromo_coords
       seq_pos_dict[chromo] = chromo_seq_pos

       check = (n_models * 3) + 1
       i = 0

     elif not chromo:
       raise Exception('Missing chromosome record in file %s' % file_path)

     elif n_items != check:
       msg = 'Data size in file %s does not match Position + Models * Positions * 3'
       raise Exception(msg % file_path)

     else:
       chromo_seq_pos[i] = int(data[0])

       coord = [float(x) for x in data[1:]]
       coord = np.array(coord).reshape(n_models, 3)
       chromo_coords[:,i] = coord
       i += 1

 return seq_pos_dict, coords_dict


def export_coords(out_format, out_file_path, coords_dict, particle_seq_pos, particle_size):
  
  # Save final coords as N3D or PDB format file
  
  if out_format == PDB:
    if not out_file_path.endswith(PDB):
      out_file_path = '%s.%s' % (out_file_path, PDB)
  
    export_pdb_coords(out_file_path, coords_dict, particle_seq_pos, particle_size)
 
  else:
    if not out_file_path.endswith(N3D):
      out_file_path = '%s.%s' % (out_file_path, N3D)
      
    export_n3d_coords(out_file_path, coords_dict, particle_seq_pos)
    
  print('Saved structure file to: %s' % out_file_path)


def calc_genome_structure(ncc_file_path, out_file_path, general_calc_params, anneal_params,
                          particle_sizes, num_models=5, isolation_threshold=2e6,
                          out_format=N3D, num_cpu=MAX_CORES,Target_Chrom=None,
                          start_coords_path=None, save_intermediate=False):

  from time import time

  # Load single-cell Hi-C data from NCC contact file, as output from NucProcess
  chromosomes, chromo_limits, contact_dict = load_pair_file(ncc_file_path,target_Chrom=Target_Chrom)

  # Only use contacts which are supported by others nearby in sequence, in the initial instance
  contact_dict = remove_isolated_contacts(contact_dict, threshold=isolation_threshold)

  # Initial coords will be random
  start_coords = None

  # Record particle positions from previous stages
  # so that coordinates can be interpolated to higher resolution
  prev_seq_pos = None

  if start_coords_path:
    prev_seq_pos, start_coords = load_n3d_coords(start_coords_path)
    if start_coords:
      chromo = next(iter(start_coords)) # picks out arbitrary chromosome
      num_models = len(start_coords[chromo])
    
  for stage, particle_size in enumerate(particle_sizes):
 
      print("Running structure caculation stage %d (%d kb)" % (stage+1, (particle_size/1e3)))
 
      # Can remove large violations (noise contacts inconsistent with structure)
      # once we have a reasonable resolution structure
      
      if stage > 0:
        if particle_size < 0.5e6:
            remove_violated_contacts(contact_dict, coords_dict, particle_seq_pos,
                                     particle_size, threshold=6.0)
        elif particle_size < 0.25e6:
            remove_violated_contacts(contact_dict, coords_dict, particle_seq_pos,
                                     particle_size, threshold=5.0)
 
      coords_dict, particle_seq_pos = anneal_genome(chromosomes, contact_dict, num_models, particle_size,
                                                    general_calc_params, anneal_params,
                                                    prev_seq_pos, start_coords, num_cpu)
 
      if save_intermediate and stage < len(particle_sizes)-1:
        file_path = '%s_%d.%s' % (out_file_path[:-4], stage, out_file_path[-3:]) # DANGER: assumes that suffix is 3 chars
        export_coords(out_format, file_path, coords_dict, particle_seq_pos, particle_size)
        
      # Next stage based on previous stage's 3D coords
      # and their respective seq. positions
      start_coords = coords_dict
      prev_seq_pos = particle_seq_pos

  # Save final coords
  export_coords(out_format, out_file_path, coords_dict, particle_seq_pos, particle_size)

