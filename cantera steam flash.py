# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 14:12:13 2022

@author: AndrewMiller
"""

Alternate Cantera calc approach

#know input kg, T, P
#know output P
import cantera as ct
x = ct.Oxygen()
x.PQ = ct.one_atm*10, 0
h1 = x.h
x.PQ = ct.one_atm*10, 1
h2 = x.h
print(h2-h1) #heat of vaporization
print(x.report())
#%%
#https://bsiengr.com/wp-content/uploads/2020/11/Flash-Steam.pdf
def flash_loss(P1, P2):
    x = ct.Oxygen()

    # P1 = ct.one_atm*2 #incoming fluid pressure
    # P2 = ct.one_atm #vent pressure of receiving tank
    
    x.PQ = P1, 0 #presume we have saturated liquid coming in (higher pressure condensate)
    T1 = x.T#incoming fluid temperature
    H_cond = x.h #enthalpy of condensate stream at P1, T1 (in this case, presuming to be sat liquid)
    
    x.PQ = P2, 0
    H_liq_sat = x.h #enthalpy of saturated liquid at P2
    x.PQ = P2, 1
    H_vapor_sat = x.h #enthalpy of saturated vapor at P2
    
    H_vaporization = H_vapor_sat - H_liq_sat #enthalpy of vaporization at P2
    
    x_flash = (H_cond-H_liq_sat)/H_vaporization
    return x_flash

losses = []
pressures = []
for i in range(20):
    i = i + 1
    loss = flash_loss(ct.one_atm*i, ct.one_atm)
    losses.append(loss)
    pressures.append(ct.one_atm*i * 0.145038/1000)
    print(loss)
    
def boiloff(tank_P, tank_Q, tank_V, heat_leak):
    #this is in kJ/kg and kJ
    #compute enthalpy of vaporization at tank conditions
    x = ct.Oxygen()
    x.PQ = tank_P, tank_Q
    specific_vol = x.v
    h_start = x.h
    h_end = h_start + heat_leak
    print("starting P " + str(x.P) + " T " +str(x.T) + " Q " + str(x.Q))

    #compute new tank conditions given change in enthalpy (added heat), constant specific volume (fixed size tank)
    #(VH term)
    x.VH = specific_vol, h_end
    print("ending   P " + str(x.P) + " T " +str(x.T) + " Q " + str(x.Q))



    #so if filling a tank with 20 liters of gas
    #we vent: the amount filled as pure displacement of the receiving tank gas
    #and also the flash losses of liquid volume to fill * flash loss fraction

import matplotlib.pyplot as plt
plt.clf()
plt.subplot(1, 1, 1)
plt.plot(pressures, losses)
plt.xlabel('Time (s)')
plt.ylabel('Temperature (K)')
#%%
def expand(fluid, p_final, eta):
    """Adiabatically expand a fluid to pressure p_final, using
    a turbine with isentropic efficiency eta."""
    h0 = fluid.h
    s0 = fluid.s
    fluid.SP =s0, p_final
    h1s = fluid.h
    isentropic_work = h0 - h1s
    actual_work = isentropic_work * eta
    h1 = h0 - actual_work
    fluid.HP = h1, p_final
    return actual_work