from ase.io import read
import numpy as np
import matplotlib.pyplot as plt
from ballistico.finitedifference import FiniteDifference
from ballistico.phonons import Phonons
from ballistico.conductivity import Conductivity
from sklearn.neighbors.kde import KernelDensity
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt 
#from ballistico.controllers.plotter import plot_dispersion

# Uncomment the following to import from lammps

# folder = 'structure_lammps'
# config_file = str(folder) + '/replicated_coords.lmp'
# dynmat_file = str(folder) + '/dynmat.dat'
# third_file = str(folder) + '/third.dat'
# atoms = read(config_file, format='lammps-data', style='atomic')
#
# atomic_numbers = atoms.get_atomic_numbers()
# atomic_numbers[atomic_numbers == 1] = 14
# atoms.set_atomic_numbers(atomic_numbers)
#
# finite_difference = FiniteDifference.from_files(replicated_atoms=atoms, dynmat_file=dynmat_file, folder=folder)

finite_difference = FiniteDifference.from_folder('structure_512', format='eskm')

# Conductivity AF
for temp in range(100,100,100):  
  phonons = Phonons(finite_difference=finite_difference,
                    is_classic=False,
                    temperature=temp,
                    # 1 THz
                    # third_bandwidth=1/4.135,
                    broadening_shape='triangle',
                    is_tf_backend=False,
                    folder='ald-output')
  
  # Unfortunately at the moment the input is in 2 * pi * THZ
  # 0.5 THz
  phonons.diffusivity_bandwidth = 0.5 * 2 * np.pi / 4.135
  cond = Conductivity(phonons=phonons, method='qhgk').conductivity.sum(axis=0)
  cond = np.abs(np.mean(cond.diagonal()))
  print('AF conductivity: ', cond)



# Conductivity QHGK
list_temp=[800,1800]
for temp in list_temp:
  phonons = Phonons(finite_difference=finite_difference,
                    is_classic=False,
                    temperature=temp,
                    # 1 THz
                    third_bandwidth=1/4.135,
                    broadening_shape='triangle',
                    is_tf_backend=False,
                    is_diffusivity_using_Mori=False,
                    is_ps_gamma_including_sigma=True,
                    folder='ald-output')
  
  phonons.diffusivity_bandwidth = phonons.bandwidth.reshape((phonons.n_k_points, phonons.n_modes))
  cond = Conductivity(phonons=phonons, method='qhgk').conductivity.sum(axis=0)
  cond = np.abs(np.mean(cond.diagonal()))
  print('QHGK conductivity: ', cond)
  print('Temperature: ', temp)
  omega = phonons._omegas.reshape(phonons.n_modes)
  ps_gamma=phonons._ps_and_gamma
  #sta stupidamente ricalcolando ps and gamma anche se li ha salvati
  nome_file='plot_third_'+str(temp)
  file_third=open(nome_file,'w')
  for i in range(len(omega)):
      print(omega[i],ps_gamma[i,1],ps_gamma[i,2],sep='  ',file=file_third)
  file_third.close()
#  #plot gamma vs frequencies
#  filenameplot='plot_omega_'+str(temp)+'.out'
#  file_plot=open(filenameplot,'a')
#  frequencies = phonons.frequency.flatten()
#  frequencies=frequencies[3:]
#  print(frequencies.shape)
#  for x in frequencies:
#    print(x,file=file_plot)
#  file_plot.close()
#  filenameplot='plot_gamma_'+str(temp)+'.out'
#  file_plot=open(filenameplot,'a')
#  gamma_classic = phonons.bandwidth.flatten()
#  gamma_classic=gamma_classic[3:]
#  print(gamma_classic.shape)
#  for x in gamma_classic:
#    print(x,file=file_plot)
#
#  plt.plot(frequencies, gamma_classic, 'b.', markersize=10)
#  plt.ylabel('$\Gamma$ (THz)', fontsize=25, fontweight='bold')
#  plt.xlabel("$\\nu$ (Thz)", fontsize=25, fontweight='bold')
#  #plt.ylim([gamma_classic.min(), 6])
#  filename='gamma_omega_'+str(temp)+'.pdf'
#  plt.savefig(filename)
#  file_plot.close()
