![licence](https://img.shields.io/github/license/Zncl2222/Stochastic_UC_SGSIM)
![python](https://img.shields.io/pypi/pyversions/uc-sgsim)
[![ci](https://img.shields.io/github/actions/workflow/status/Zncl2222/uc_sgsim/github-pre-commit.yml?logo=pre-commit&label=pre-commit)](https://github.com/Zncl2222/Stochastic_UC_SGSIM/actions/workflows/github-pre-commit.yml)
[![build](https://img.shields.io/github/actions/workflow/status/Zncl2222/uc_sgsim/cmake.yml?logo=cmake&logoColor=red&label=CMake)](https://github.com/Zncl2222/Stochastic_UC_SGSIM/actions/workflows/cmake.yml)
[![pytest](https://img.shields.io/github/actions/workflow/status/Zncl2222/uc_sgsim/sonarcloud.yml?logo=pytest&label=pytest)](https://github.com/Zncl2222/Stochastic_UC_SGSIM/actions/workflows/sonarcloud.yml)
[![build](https://github.com/Zncl2222/Stochastic_UC_SGSIM/actions/workflows/codeql.yml/badge.svg)](https://github.com/Zncl2222/Stochastic_UC_SGSIM/actions/workflows/codeql.yml)
[![codecov](https://codecov.io/gh/Zncl2222/uc_sgsim/branch/main/graph/badge.svg?token=3qZt0OqDNI)](https://codecov.io/gh/Zncl2222/uc_sgsim)

<div>
 <table>
  <thead>
    <tr>
      <td colspan="5" align="center"><strong>Sonar Cloud Quality</strong></td>
    </tr>
    <tr>
      <th>Metric</th>
      <th>Python</th>
      <th>C</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Quality Gate</strong></td>
      <td><a href="https://sonarcloud.io/summary/new_code?id=zncl2222_Stochastic_UC_SGSIM_py"><img src="https://sonarcloud.io/api/project_badges/measure?project=zncl2222_Stochastic_UC_SGSIM_py&metric=alert_status" alt="Quality Gate Status"></a></td>
      <td><a href="https://sonarcloud.io/summary/new_code?id=zncl2222_Stochastic_UC_SGSIM_c"><img src="https://sonarcloud.io/api/project_badges/measure?project=zncl2222_Stochastic_UC_SGSIM_c&metric=alert_status" alt="Quality Gate Status"></a></td>
    <tr>
      <td><strong>Reliability Rating</strong></td>
      <td><a href="https://sonarcloud.io/summary/new_code?id=zncl2222_Stochastic_UC_SGSIM_py"><img src="https://sonarcloud.io/api/project_badges/measure?project=zncl2222_Stochastic_UC_SGSIM_py&metric=reliability_rating" alt="Reliability Rating"></a></td>
      <td><a href="https://sonarcloud.io/summary/new_code?id=zncl2222_Stochastic_UC_SGSIM_c"><img src="https://sonarcloud.io/api/project_badges/measure?project=zncl2222_Stochastic_UC_SGSIM_c&metric=reliability_rating" alt="Reliability Rating"></a></td>
    </tr>
    <tr>
      <td><strong>Security Rating</strong></td>
      <td><a href="https://sonarcloud.io/summary/new_code?id=zncl2222_Stochastic_UC_SGSIM_py"><img src="https://sonarcloud.io/api/project_badges/measure?project=zncl2222_Stochastic_UC_SGSIM_py&metric=security_rating" alt="Security Rating"></a></td>
      <td><a href="https://sonarcloud.io/summary/new_code?id=zncl2222_Stochastic_UC_SGSIM_c"><img src="https://sonarcloud.io/api/project_badges/measure?project=zncl2222_Stochastic_UC_SGSIM_c&metric=security_rating" alt="Security Rating"></a></td>
    </tr>
    <tr>
      <td><strong>Maintainability Rating</strong></td>
      <td><a href="https://sonarcloud.io/summary/new_code?id=zncl2222_Stochastic_UC_SGSIM_py"><img src="https://sonarcloud.io/api/project_badges/measure?project=zncl2222_Stochastic_UC_SGSIM_py&metric=sqale_rating" alt="Maintainability Rating"></a></td>
      <td><a href="https://sonarcloud.io/summary/new_code?id=zncl2222_Stochastic_UC_SGSIM_c"><img src="https://sonarcloud.io/api/project_badges/measure?project=zncl2222_Stochastic_UC_SGSIM_c&metric=sqale_rating" alt="Maintainability Rating"></a></td>
    </tr>
  </tbody>
 </table>
</div>

<h3 align="center">

> __Warning__
> This project is still in the pre-dev stage, the API usuage may be subject to change

</h3>

## UnConditional Sequential Gaussian SIMulation (UCSGSIM)

<h3 align="center">An unconditional random field generation tools that are easy to use.</h3>

## Introduction to UCSGSIM
UnConditional Sequential Gaussian Simulation (UCSGSIM) is a method for generating random fields that is based on the kriging interpolation technique.

Unconditional simulation does not adhere to the patterns observed in the data but instead follows the user's settings, such as mean and variance.

**The core ideas of UCSGSIM are:**
1. Create the grid (no data values exist at this stage).

$$ \Omega\to R $$

2. Select a random point within the model (draw one random value from the x_grid).

$$ X = RandomValue(\Omega),  X:\Omega\to R $$

3. Choose the **theoretical covariance model** to use and set the **sill** and **range** properly.

$$ Gaussian = (C_{0} - s)(1 - e^{-h^{2}/r^{2}a})$$

$$ Spherical = (C_{0} - s)(3h/2r - h^3/2r^3)$$

$$ Exponential = (C_{0} - s)(1 - e^{-h/ra})$$

4. If there are more than one data value close to the visited point (based on the **range** of the covariance model), proceed to the next step. Otherwise, draw a random value from a normal distribution as the simulation result for this iteration.

$$ Z_{k}({X_{simulation}}) = RandomNormal(m = 0 ,\sigma^2 = Sill)$$

5. Calculate **weights** from the **data covaraince** and **distance coavariance**

$$ \sum_{j=1}^{n}\omega_{j} = C(X_{data}^{i},X_{data}^{i})C^{-1}(X_i,X_i), i=1...N $$

6. Calculate the **kriging estimate** from the **weights** and **data value**

$$ Z_{k}(X_{estimate}) = \sum_{i=1}^{n} \omega_{i} Z(X_{data}) + (1- \sum_{i=1}^{n} \omega_{i} m_{g}) $$

7. Calculate the **kriging error (kriging variance)** from **weights** and **data covariance**

$$ \sigma_{krige}^{2} = \sum_{i=1}^{n}\omega_{i}C(X_{data}^{i},X_{data}^{i}) $$

8. Draw a random value from the normal distribution and add to the **kriging estimate**.

$$ Z(X_{simulation}) = Z(X_{estimate}) + RandomNormal(m = 0, \sigma^2 = \sigma_{krige}^{2}) $$

9. Repeat 2 ~ 8 until the entire model is simulated.

10. Repeat 1 ~ 9 with different **randomseed number** to produce mutiple realizations.

## Installation
```bash
pip install uc-sgsim
```

## Features
* One dimensional unconditional randomfield generation with sequential gaussian simulation algorithm
* Muti-cores simulation (mutiprocessing)
* Ability to generate random fields in Python using either a C interface via ctype or directly in Python using the NumPy and SciPy libraries.

## Examples
```py
import matplotlib.pyplot as plt
import uc_sgsim as uc
from uc_sgsim.cov_model import Gaussian

if __name__ == '__main__':
    x = 151  # Model grid, only 1D case is support now

    bw_s = 1  # lag step
    bw_l = 35  # lag range
    randomseed = 151  # randomseed for simulation
    k_range = 17.32  # effective range of covariance model
    sill = 1  # sill of covariance model

    nR = 10  # numbers of realizations in each CPU cores,
    # if nR = 1 n_process = 8
    # than you will compute total 8 realizations

    # Create Covariance model first
    cov_model = Gaussian(bw_l, bw_s, k_range, sill)

    # Create simulation and input the Cov model
    # You could also set z_min, z_max and max_neighbor for sgsim by key words
    # sgsim = uc.UCSgsimDLL(x, nR, cov_model, z_min=-6, z_max=6, max_neigh=10)
    # set z_min, z_max and max_neighbor by directly assign
    # sgsim.z_min = -6
    # sgsim.z_max = 6
    # sgsim.max_neigh = 10

    # Create simulation with default z_min, z_max and max_neigh params
    sgsim_py = uc.UCSgsim(x, nR, cov_model) # run sgsim with python
    sgsim_c = uc.UCSgsimDLL(x, nR, cov_model) # run sgsim with c

    # Start compute with n CPUs
    sgsim_c.compute(n_process=2, randomseed=randomseed)
    sgsim_py.compute(n_process=2, randomseed=987654)

    sgsim_c.mean_plot('ALL')  # Plot mean
    sgsim_c.variance_plot()  # Plot variance
    sgsim_c.cdf_plot(x_location=10)  # CDF
    sgsim_c.hist_plot(x_location=10)  # Hist
    sgsim_c.variogram_compute(n_process=2)  # Compute variogram before plotting
    # Plot variogram and mean variogram for validation
    sgsim.variogram_plot()
    # Save random_field and variogram
    sgsim_c.save_random_field('randomfields.csv', save_single=True)
    sgsim_c.save_variogram('variograms.csv', save_single=True)

    # show figure
    plt.show()
```

<p align="center">
   <img src="https://github.com/Zncl2222/Stochastic_SGSIM/blob/main/figure/Realizations.png"  width="40%"/>
   <img src="https://github.com/Zncl2222/Stochastic_SGSIM/blob/main/figure/Mean.png"  width="40%"/>
   <img src="https://github.com/Zncl2222/Stochastic_SGSIM/blob/main/figure/Variance.png"  width="40%"/>
   <img src="https://github.com/Zncl2222/Stochastic_SGSIM/blob/main/figure/Variogram.png"  width="50%"/>
   <img src="https://github.com/Zncl2222/Stochastic_SGSIM/blob/main/figure/HIST.png"  width="40%"/>
   <img src="https://github.com/Zncl2222/Stochastic_SGSIM/blob/main/figure/CDF.png"  width="50%"/>
</p>

If you prefer to utilize pure C to execute this code, you can make modifications to the c_example.c file located in the root directory. Once you've made the necessary changes to c_example.c, you can compile and execute the code using the following commands:

On Linux
```bash
sh cmake_build.sh
```
On Windows
```bat
cmake_build.bat
```

C example file
```c
// c_example.c
# include <stdio.h>
# include <stdlib.h>

# include "./uc_sgsim/c_core/include/sgsim.h"
# include "./uc_sgsim/c_core/include/cov_model.h"
# if defined(__linux__) || defined(__unix__)
# define PAUSE printf("Press Enter key to continue..."); fgetc(stdin);//NOLINT
# elif _WIN32
# define PAUSE system("PAUSE");
# endif

int main() {
    // you can also set z_min and z_max at sgsim_t. Default value will depend on
    // sill value in cov_model_t
    sgsim_t sgsim_example = {
        .x_len = 150,
        .realization_numbers = 5,
        .randomseed = 12345,
        .kriging_method = 1,
        .if_alloc_memory = 1,  // This should be equal to 1 if you want to run by c.
    };

    // you can also set max_negibor at cov_model_t. Defualt value is 4.
    cov_model_t cov_example = {
        .bw_l = 35,
        .bw_s = 1,
        .k_range = 17.32,
        .use_cov_cache = 0,
        .sill = 1,
        .nugget = 0,
    };

    sgsim_run(&sgsim_example, &cov_example, 0);
    sgsim_t_free(&sgsim_example);
    PAUSE
    return 0;
}
```

## Future plans
* 2D unconditional randomfield generation
* GUI (pyhton)
* More covariance models
* More kriging methods (etc. Oridinary Kriging)
* Performance enhancement
* Providing more comprehensive documentation and user-friendly design improvements.

## Performance
<p align="center">
<img src="https://github.com/Zncl2222/Stochastic_SGSIM/blob/main/figure/C_Cpp_py_comparision.png"  width="70%"/>
</p>

```
Parameters:

model len = 150

number of realizations = 1000

Range scale = 17.32

Variogram model = Gaussian model

---------------------------------------------------------------------------------------

Testing platform:

CPU: AMD Ryzen 9 4900 hs

RAM: DDR4 - 3200 40GB (Dual channel 16GB)

Disk: WD SN530
```
