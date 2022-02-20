# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 18:27:34 2022

@author: Minja
"""
import numpy as np

timestamp = 1
x = 2
y = 3
Ts =  16667

def idt(data, dis_threshold, dur_threshold):

	window_range = [0,0]

	current = 0 #pocetna vrednost prozora
	last = 0
	#liste za fiksacije 
	centroidsX = []
	centroidsY = []
	time0 = []
	time1 = []
	fix_duration = []
	fix_counts = []
    
	while (current < len(data)):
        
		t0 = float(data.iloc[current, timestamp]) #pocetno vreme
		t1 = t0 + float(dur_threshold)   #krajnje vreme - dodat je treshold

		for r in range(current, len(data)): 
			if(float(data.iloc[r,timestamp])>= t0 and float(data.iloc[r,timestamp])<= t1):
				last = r #pronalazi poslednji indeks koji ispunjava uslov da je unutar opsega od 0 do dur_treshold

		window_range = [current,last]

		# Trazimo disperziju prozora
		dispersion = get_dispersion(data.iloc[current:last+1])
        
		if (dispersion <= dis_threshold):

			# Dodajemo nove tacke
			while(dispersion <= dis_threshold and last + 1 < len(data)):

				last += 1
				window_range = [current,last]
				dispersion = get_dispersion(data.iloc[current:last+1])
       
			# Trazimo centar mase prozora fiksacija

			cX = 0
			cY = 0
            
			for f in range(current, last + 1):
				cX += float(data.iloc[f,x])
				cY += float(data.iloc[f,y])

			cX = cX / float(last - current + 1)
			cY = cY / float(last - current + 1)
                
			t0 = float(data.iloc[current,timestamp])
			t1 = float(data.iloc[last,timestamp])
			fix_time = t1 - t0
			fix_count = np.ceil((t1 - t0)/Ts)
            
			centroidsX.append(cX)
			centroidsY.append(cY)
			time0.append(t0)
			time1.append(t1)
			fix_duration.append(fix_time)
			fix_counts.append(fix_count)
            
			current = last + 1 #pomera ga na novi prozor

		else:
			current += 1 # uklanja prvu tacku (smatra se da je sakada)
			last = current
            
	return centroidsX, centroidsY, time0, time1, fix_counts, fix_duration

def get_dispersion(points):

	dispersion = 0
    
	argxmin = np.min(points.iloc[:,x].astype(np.float))
	argxmax = np.max(points.iloc[:,x].astype(np.float))
    
	argymin = np.min(points.iloc[:,y].astype(np.float))
	argymax = np.max(points.iloc[:,y].astype(np.float))

	dispersion = (argxmax - argxmin) + (argymax - argymin)
    
	return dispersion

