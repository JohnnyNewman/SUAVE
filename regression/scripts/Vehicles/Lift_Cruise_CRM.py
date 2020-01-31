# Lift_Cruise_CRM.py
# 
# Created: May 2019, M Clarke

#----------------------------------------------------------------------
#   Imports
# ---------------------------------------------------------------------
import SUAVE
from SUAVE.Core import Units, Data
import copy
from SUAVE.Components.Energy.Networks.Lift_Cruise import Lift_Cruise
from SUAVE.Methods.Power.Battery.Sizing import initialize_from_mass
from SUAVE.Methods.Propulsion.electric_motor_sizing import size_from_mass
from SUAVE.Methods.Propulsion import propeller_design   
from SUAVE.Methods.Weights.Buildups.Electric_Lift_Cruise.empty import empty
import numpy as np
from copy import deepcopy

# ----------------------------------------------------------------------
#   Build the Vehicle
# ----------------------------------------------------------------------
def vehicle_setup():
    
    # ------------------------------------------------------------------
    #   Initialize the Vehicle
    # ------------------------------------------------------------------    
    vehicle               = SUAVE.Vehicle()
    vehicle.tag           = 'Lift_Cruise_CRM'
    vehicle.configuration = 'eVTOL'
    # ------------------------------------------------------------------
    #   Vehicle-level Properties
    # ------------------------------------------------------------------    
    # mass properties
    vehicle.mass_properties.takeoff           = 3000. * Units.lb 
    vehicle.mass_properties.operating_empty   = 2000. * Units.lb               # Approximate
    vehicle.mass_properties.max_takeoff       = 3000. * Units.lb               # Approximate
    vehicle.mass_properties.center_of_gravity = [8.5*0.3048 ,   0.  ,  0.*0.3048 ] # Approximate
    
    # basic parameters
    vehicle.passengers                        = 5
    vehicle.reference_area                    = 11.13172471 * Units.feet**2		
    vehicle.envelope.ultimate_load            = 5.7   
    vehicle.envelope.limit_load               = 3.  
    
    # ------------------------------------------------------				
    # WINGS				
    # ------------------------------------------------------				
    # WING PROPERTIES	
    wing = SUAVE.Components.Wings.Main_Wing()
    wing.tag	                  = 'main_wing'		
    wing.aspect_ratio	          = 10.76 
    wing.sweeps.quarter_chord	  = 0.0	 * Units.degrees
    wing.thickness_to_chord	  = 0.18		
    wing.taper	                  = 1. 	
    wing.span_efficiency	  = 0.9		
    wing.spans.projected	  = 35.0   * Units.feet
    wing.chords.root	          = 3.25   * Units.feet
    wing.total_length	          = 3.25   * Units.feet	
    wing.chords.tip	          = 3.25   * Units.feet	
    wing.chords.mean_aerodynamic  = 3.25   * Units.feet		
    wing.dihedral	          = 1.0    * Units.degrees		
    wing.areas.reference	  = 113.75 * Units.feet**2	
    wing.areas.wetted	          = 227.5  * Units.feet**2		
    wing.areas.exposed	          = 227.5  * Units.feet**2		
    wing.twists.root	          = 4.0    * Units.degrees		
    wing.twists.tip	          = 0.0    * Units.degrees			
    wing.origin	                  = [1.5, 0., 0. ] 
    wing.aerodynamic_center	  = [1.975 , 0., 0.]    
    wing.winglet_fraction         = 0.0  
    wing.symmetric                = True
    wing.vertical                 = False
    
    # Segment 	
    segment = SUAVE.Components.Wings.Segment()
    segment.tag			  = 'Section_1'			
    segment.percent_span_location = 0.		
    segment.twist		  = 0.		
    segment.root_chord_percent	  = 1.5	
    segment.dihedral_outboard	  = 1.0     * Units.degrees
    segment.sweeps.quarter_chord  = 8.5     * Units.degrees
    segment.thickness_to_chord	  = 0.18		
    wing.Segments.append(segment)
    
    # Segment 
    segment = SUAVE.Components.Wings.Segment()
    segment.tag			  = 'Section_2'				
    segment.percent_span_location = 0.227	
    segment.twist		  = 0.		
    segment.root_chord_percent	  = 1. 	
    segment.dihedral_outboard	  = 1.0  * Units.degrees
    segment.sweeps.quarter_chord  = 0.0	 * Units.degrees	
    segment.thickness_to_chord	  = 0.12	
    wing.Segments.append(segment)
                          
    # Segment 
    segment = SUAVE.Components.Wings.Segment()
    segment.tag			  = 'Section_3'			
    segment.percent_span_location = 1.0 
    segment.twist		  = 0.		
    segment.root_chord_percent	  = 1.0 
    segment.dihedral_outboard	  = 1.0  * Units.degrees
    segment.sweeps.quarter_chord  = 0.0 * Units.degrees
    segment.thickness_to_chord	  = 0.12	
    wing.Segments.append(segment) 
       
    # add to vehicle
    vehicle.append_component(wing)       
    
    # WING PROPERTIES
    wing = SUAVE.Components.Wings.Wing()
    wing.tag		         = 'horizontal_tail'		
    wing.aspect_ratio		 = 4.0	
    wing.sweeps.quarter_chord	 = 0.0		
    wing.thickness_to_chord	 = 0.12		
    wing.taper			 = 1.0		
    wing.span_efficiency	 = 0.9		
    wing.spans.projected	 = 8.0	 * Units.feet
    wing.chords.root		 = 2.0	 * Units.feet	
    wing.total_length		 = 2.0	 * Units.feet	
    wing.chords.tip		 = 2.0	 * Units.feet	
    wing.chords.mean_aerodynamic = 2.0	 * Units.feet			
    wing.dihedral		 = 0.	 * Units.degrees		
    wing.areas.reference	 = 16.0  * Units.feet**2	
    wing.areas.wetted		 = 32.0  * Units.feet**2	 		
    wing.areas.exposed		 = 32.0  * Units.feet**2	 
    wing.twists.root		 = 0.	 * Units.degrees		
    wing.twists.tip		 = 0.	 * Units.degrees		
    wing.origin		         = [14.0*0.3048 , 0.0 , 0.205 ] 		
    wing.aerodynamic_center	 = [15.0*0.3048 ,  0.,  0.] 
    wing.symmetric               = True    
    
    # add to vehicle
    vehicle.append_component(wing)    
    
    
    # WING PROPERTIES
    wing = SUAVE.Components.Wings.Wing()
    wing.tag		         = 'vertical_tail_1'
    wing.aspect_ratio		 = 2.	
    wing.sweeps.quarter_chord	 = 20.0 * Units.degrees	
    wing.thickness_to_chord	 = 0.12
    wing.taper			 = 0.5
    wing.span_efficiency	 = 0.9 
    wing.spans.projected	 = 3.0	* Units.feet	
    wing.chords.root		 = 2.0	* Units.feet		
    wing.total_length		 = 2.0	* Units.feet	
    wing.chords.tip		 = 1.0	* Units.feet		
    wing.chords.mean_aerodynamic = 1.5	* Units.feet
    wing.areas.reference	 = 4.5 	* Units.feet**2
    wing.areas.wetted		 = 9.0 	* Units.feet**2	
    wing.areas.exposed		 = 9.0 	* Units.feet**2	
    wing.twists.root		 = 0.	* Units.degrees	
    wing.twists.tip		 = 0.	* Units.degrees		
    wing.origin		         = [14.0*0.3048 , 4.0*0.3048  , 0.205  ] 		
    wing.aerodynamic_center	 = 0.0 		
    wing.winglet_fraction        = 0.0  
    wing.vertical		 = True	
    wing.symmetric               = False
    
    # add to vehicle
    vehicle.append_component(wing)   
    
    
    # WING PROPERTIES
    wing = SUAVE.Components.Wings.Wing()
    wing.tag		         = 'vertical_tail_2'
    wing.aspect_ratio		 = 2.	
    wing.sweeps.quarter_chord	 = 20.0 * Units.degrees	
    wing.thickness_to_chord	 = 0.12
    wing.taper			 = 0.5
    wing.span_efficiency	 = 0.9 
    wing.spans.projected	 = 3.0	* Units.feet	
    wing.chords.root		 = 2.0	* Units.feet		
    wing.total_length		 = 2.0	* Units.feet	
    wing.chords.tip		 = 1.0	* Units.feet		
    wing.chords.mean_aerodynamic = 1.5	* Units.feet
    wing.areas.reference	 = 4.5 	* Units.feet**2
    wing.areas.wetted		 = 9.0 	* Units.feet**2	
    wing.areas.exposed		 = 9.0 	* Units.feet**2	
    wing.twists.root		 = 0.	* Units.degrees		
    wing.twists.tip		 = 0.	* Units.degrees			
    wing.origin		         = [14.0*0.3048 , -4.0*0.3048  , 0.205   ] 	
    wing.aerodynamic_center	 = 0.0 		
    wing.winglet_fraction        = 0.0  
    wing.vertical		 = True	  
    wing.symmetric               = False
    
    # add to vehicle
    vehicle.append_component(wing)   
    
    
    # ------------------------------------------------------				
    # FUSELAGE				
    # ------------------------------------------------------				
    # FUSELAGE PROPERTIES
    fuselage = SUAVE.Components.Fuselages.Fuselage()
    fuselage.tag                                = 'fuselage'
    fuselage.configuration	                = 'Tube_Wing'		
    fuselage.origin	                        = [[0. , 0.,  0.]]	
    fuselage.seats_abreast	                = 2.		
    fuselage.seat_pitch  	                = 3.		
    fuselage.fineness.nose	                = 0.88 		
    fuselage.fineness.tail	                = 1.13 		
    fuselage.lengths.nose	                = 3.2   * Units.feet	
    fuselage.lengths.tail	                = 6.4 	* Units.feet
    fuselage.lengths.cabin	                = 6.4 	* Units.feet	
    fuselage.lengths.total	                = 16.0 	* Units.feet	
    fuselage.width	                        = 5.85  * Units.feet	
    fuselage.heights.maximum	                = 4.65  * Units.feet		
    fuselage.heights.at_quarter_length	        = 3.75  * Units.feet 	
    fuselage.heights.at_wing_root_quarter_chord	= 4.65  * Units.feet	
    fuselage.heights.at_three_quarters_length	= 4.26  * Units.feet	
    fuselage.areas.wetted	                = 236.  * Units.feet**2	
    fuselage.areas.front_projected	        = 0.14  * Units.feet**2	  	
    fuselage.effective_diameter 	        = 5.85  * Units.feet 	
    fuselage.differential_pressure	        = 0.	
    
    # Segment 	
    segment = SUAVE.Components.Fuselages.Segment() 
    segment.tag			                = 'segment_1'		
    segment.origin	                        = [0., 0. ,0.]		
    segment.percent_x_location	                = 0.		
    segment.percent_z_location	                = 0.0	
    segment.height		                = 0.1   * Units.feet 		
    segment.width		                = 0.1	* Units.feet 	 		
    segment.length		                = 0.		
    segment.effective_diameter	                = 0.1	* Units.feet 		
    fuselage.Segments.append(segment)  
                          
    # Segment 
    segment = SUAVE.Components.Fuselages.Segment()
    segment.tag			                = 'segment_2'		
    segment.origin		                = [4.*0.3048 , 0. ,0.1*0.3048 ] 	
    segment.percent_x_location	                = 0.25 	
    segment.percent_z_location	                = 0.05 
    segment.height		                = 3.75  * Units.feet 
    segment.width		                = 5.65  * Units.feet 	
    segment.length		                = 3.2   * Units.feet 	
    segment.effective_diameter	                = 5.65 	* Units.feet 
    fuselage.Segments.append(segment)  
                          
    # Segment 
    segment = SUAVE.Components.Fuselages.Segment()
    segment.tag			                =' segment_3'		
    segment.origin		                = [8.*0.3048 , 0. ,0.34*0.3048 ] 	
    segment.percent_x_location	                = 0.5 	
    segment.percent_z_location	                = 0.071 
    segment.height		                = 4.65  * Units.feet	
    segment.width		                = 5.55  * Units.feet 	
    segment.length		                = 3.2   * Units.feet
    segment.effective_diameter	                = 5.55  * Units.feet 
    fuselage.Segments.append(segment)  
                          
    # Segment 	
    segment = SUAVE.Components.Fuselages.Segment()
    segment.tag			                = 'segment_4'		
    segment.origin		                = [12.*0.3048 , 0. ,0.77*0.3048 ] 
    segment.percent_x_location	                = 0.75 
    segment.percent_z_location	                = 0.089 	
    segment.height		                = 4.73  * Units.feet		
    segment.width		                = 4.26  * Units.feet 		
    segment.length		                = 3.2   * Units.feet 	
    segment.effective_diameter	                = 4.26  * Units.feet 
    fuselage.Segments.append(segment)  
                          
    # Segment
    segment = SUAVE.Components.Fuselages.Segment()
    segment.tag			                = 'segment_5'		
    segment.origin		                = [16.*0.3048 , 0. ,2.02*0.3048 ] 
    segment.percent_x_location	                = 1.0
    segment.percent_z_location	                = 0.158 
    segment.height		                = 0.67	* Units.feet
    segment.width		                = 0.33	* Units.feet
    segment.length		                = 3.2   * Units.feet	
    segment.effective_diameter	                = 0.33  * Units.feet
    fuselage.Segments.append(segment)   
    
    # add to vehicle
    vehicle.append_component(fuselage)    
    
    #-------------------------------------------------------------------
    # BOOMS			
    #-------------------------------------------------------------------   
    boom = SUAVE.Components.Fuselages.Fuselage()
    boom.tag                                    = 'Boom_1R'
    boom.configuration	                        = 'Boom'		
    boom.origin	                                = [[0.718,7.5*0.3048 , -0.15 ]]
    boom.seats_abreast	                        = 0.		
    boom.seat_pitch	                        = 0.0	
    boom.fineness.nose	                        = 0.950 		
    boom.fineness.tail	                        = 1.029 		
    boom.lengths.nose	                        = 0.5   * Units.feet			
    boom.lengths.tail	                        = 0.5   * Units.feet	 		
    boom.lengths.cabin	                        = 9.	* Units.feet
    boom.lengths.total	                        = 10    * Units.feet			
    boom.width	                                = 0.5	* Units.feet			
    boom.heights.maximum                        = 0.5	* Units.feet			
    boom.heights.at_quarter_length	        = 0.5	* Units.feet			
    boom.heights.at_three_quarters_length	= 0.5	* Units.feet
    boom.heights.at_wing_root_quarter_chord     = 0.5   * Units.feet
    boom.areas.wetted		                = 18 	* Units.feet**2
    boom.areas.front_projected	                = 0.26 	* Units.feet**2
    boom.effective_diameter	                = 0.5	* Units.feet	 		
    boom.differential_pressure	                = 0.	
    boom.y_pitch_count                          = 2
    boom.y_pitch                                = (72/12)*0.3048
    boom.symmetric                              = True
    boom.boom_pitch                             = 6 * Units.feet
    boom.index = 1 
                                                
    # add to vehicle
    vehicle.append_component(boom)    
    
    # create pattern of booms on one side
    original_boom_origin =  boom.origin	
    if boom.y_pitch_count >  1 : 
        for n in range(boom.y_pitch_count):
            if n == 0:
                continue
            else:
                index = n+1
                boom = deepcopy(vehicle.fuselages.boom_1r)
                boom.origin[0][1] = n*boom.boom_pitch + original_boom_origin[0][1]
                boom.tag = 'Boom_' + str(index) + 'R'
                boom.index = n 
                vehicle.append_component(boom)
    
    if boom.symmetric : 
        for n in range(boom.y_pitch_count):
            index = n+1
            boom = deepcopy(vehicle.fuselages.boom_1r)
            boom.origin[0][1] = -n*boom.boom_pitch - original_boom_origin[0][1]
            boom.tag = 'Boom_' + str(index) + 'L'
            boom.index = n 
            vehicle.append_component(boom) 
            
            
    #------------------------------------------------------------------
    # PROPULSOR
    #------------------------------------------------------------------
    net = Lift_Cruise()
    net.number_of_engines_lift    = 8
    net.number_of_engines_forward = 1
    net.thrust_angle_lift         = 90. * Units.degrees
    net.thrust_angle_forward      = 0. 
    net.nacelle_diameter          = 0.6 * Units.feet	# need to check	
    net.engine_length             = 0.5 * Units.feet
    net.areas                     = Data()
    net.areas.wetted              = np.pi*net.nacelle_diameter*net.engine_length + 0.5*np.pi*net.nacelle_diameter**2    
    net.voltage = 400.

    #------------------------------------------------------------------
    # Design Electronic Speed Controller 
    #------------------------------------------------------------------
    esc_lift                     = SUAVE.Components.Energy.Distributors.Electronic_Speed_Controller()
    esc_lift.efficiency          = 0.95
    net.esc_lift                 = esc_lift

    esc_thrust                   = SUAVE.Components.Energy.Distributors.Electronic_Speed_Controller()
    esc_thrust.efficiency        = 0.95
    net.esc_forward              = esc_thrust

    #------------------------------------------------------------------
    # Design Payload
    #------------------------------------------------------------------
    payload                      = SUAVE.Components.Energy.Peripherals.Avionics()
    payload.power_draw           = 0.
    payload.mass_properties.mass = 200. * Units.kg
    net.payload                  = payload

    #------------------------------------------------------------------
    # Design Avionics
    #------------------------------------------------------------------
    avionics                     = SUAVE.Components.Energy.Peripherals.Avionics()
    avionics.power_draw          = 200. * Units.watts
    net.avionics                 = avionics

    #------------------------------------------------------------------
    # Design Battery
    #------------------------------------------------------------------
    bat                          = SUAVE.Components.Energy.Storages.Batteries.Constant_Mass.Lithium_Ion()
    bat.specific_energy          = 300. * Units.Wh/Units.kg
    bat.resistance               = 0.005
    bat.max_voltage              = 400.
    bat.mass_properties.mass     = 300. * Units.kg
    initialize_from_mass(bat, bat.mass_properties.mass)
    net.battery                  = bat

    #------------------------------------------------------------------
    # Design Rotors and Propellers
    #------------------------------------------------------------------
    # Thrust Propeller
    prop_forward                     = SUAVE.Components.Energy.Converters.Propeller()
    prop_forward.tag                 = 'Forward_Prop'
    prop_forward.symmetric           = False
    prop_forward.tip_radius          = 3.0   * Units.feet
    prop_forward.hub_radius          = 0.6   * Units.feet
    prop_forward.number_blades       = 3
    prop_forward.freestream_velocity = 110.  * Units['mph']  
    prop_forward.angular_velocity    = 2000. * Units['rpm']          
    prop_forward.design_Cl           = 0.7
    prop_forward.design_altitude     = 1000  * Units.feet                           
    prop_forward.design_thrust       = 2500       
    prop_forward.design_power        = 0.0                         
    prop_forward                     = propeller_design(prop_forward)     
    prop_forward.origin              = vehicle.fuselages['fuselage'].Segments['segment_5'].origin 
    
    if prop_forward.symmetric: 
        for n in range(len(prop_forward.origin)):
            prop_origin = [prop_forward.origin[n][0] , -prop_forward.origin[n][1] ,prop_forward.origin[n][2]]
            prop_forward.origin.append(prop_origin)     
    net.propeller_forward    = prop_forward
    
    # Lift Rotors
    prop_lift                        = SUAVE.Components.Energy.Converters.Propeller()
    prop_lift.tag                    = 'Lift_Prop'
    prop_lift.tip_radius             = 2.8 * Units.feet
    prop_lift.hub_radius             = 0.6 * Units.feet      
    prop_lift.number_blades          = 2    
    vehicle_weight                   = vehicle.mass_properties.takeoff*9.81*0.453592    
    rho                              = 1.2
    prop_lift.disc_area              = np.pi*(prop_lift.tip_radius**2)    
    prop_lift.induced_hover_velocity = np.sqrt(vehicle_weight/(2*rho*prop_lift.disc_area*net.number_of_engines_lift)) 
    prop_lift.freestream_velocity    = prop_lift.induced_hover_velocity 
    prop_lift.angular_velocity       = 3100. * Units['rpm']      
    prop_lift.design_Cl              = 0.7
    prop_lift.design_altitude        = 20    * Units.feet                            
    prop_lift.design_thrust          = (vehicle.mass_properties.takeoff/net.number_of_engines_lift)*0.453592*9.81*1.2
    prop_lift.design_power           = 0.0                         
    prop_lift.symmetric              = True
    prop_lift.x_pitch_count          = 2
    prop_lift.y_pitch_count          = vehicle.fuselages['boom_1r'].y_pitch_count
    prop_lift.y_pitch                = vehicle.fuselages['boom_1r'].y_pitch 
    prop_lift                        = propeller_design(prop_lift)          
    prop_lift.origin                 = vehicle.fuselages['boom_1r'].origin
   
    # populating propellers on one side of wing
    if prop_lift.y_pitch_count > 1 :
        for n in range(prop_lift.y_pitch_count):
            if n == 0:
                continue
            proppeller_origin = [prop_lift.origin[0][0] , prop_lift.origin[0][1] +  n*prop_lift.y_pitch ,prop_lift.origin[0][2]]
            prop_lift.origin.append(proppeller_origin)   
   
   
    # populating propellers on one side of the vehicle 
    if prop_lift.x_pitch_count > 1 :
        relative_prop_origins = np.linspace(0,vehicle.fuselages['boom_1r'].lengths.total,prop_lift.x_pitch_count)
        for n in range(len(prop_lift.origin)):
            for m in range(len(relative_prop_origins)-1):
                proppeller_origin = [prop_lift.origin[n][0] + relative_prop_origins[m+1] , prop_lift.origin[n][1] ,prop_lift.origin[n][2] ]
                prop_lift.origin.append(proppeller_origin)
                 
    # propulating propellers on the other side of thevehicle   
    if prop_lift.symmetric : 
        for n in range(len(prop_lift.origin)):
            proppeller_origin = [prop_lift.origin[n][0] , -prop_lift.origin[n][1] ,prop_lift.origin[n][2] ]
            prop_lift.origin.append(proppeller_origin) 
    
    # re compute number of lift propellers if changed 
    net.number_of_engines_lift    = len(prop_lift.origin)        
    
    # append propellers to vehicle     
    net.propeller_lift            = prop_lift
    
    #------------------------------------------------------------------
    # Design Motors
    #------------------------------------------------------------------
    # Thrust motor
    etam                              = 0.95
    v                                 = bat.max_voltage *3/4
    omeg                              = 2500. * Units.rpm
    kv                                = 8.5   * Units.rpm
    io                                = 2.0                                      
    res                               = ((v-omeg/kv)*(1.-etam*v*kv/omeg))/io
    
    motor_forward                      = SUAVE.Components.Energy.Converters.Motor()
    motor_forward.mass_properties.mass = 25. * Units.kg                         
    motor_forward.origin               = vehicle.fuselages['fuselage'].Segments['segment_5'].origin 
    motor_forward.speed_constant       = kv
    motor_forward.resistance           = res
    motor_forward.no_load_current      = io  
    motor_forward.gear_ratio           = 1.0
    motor_forward.propeller_radius     = prop_forward.tip_radius
    net.motor_forward                  = motor_forward

    #Lift Motor
    etam                              = 0.95
    v                                 = bat.max_voltage 
    omeg                              = 3000. * Units.rpm
    kv                                = 7.6 * Units.rpm
    io                                = 4.0
    res                               = ((v-omeg/kv)*(1.-etam*v*kv/omeg))/io 
    
    motor_lift                        = SUAVE.Components.Energy.Converters.Motor()
    motor_lift.mass_properties.mass   = 3. * Units.kg
    motor_lift.origin                 = prop_lift.origin    
    motor_lift.speed_constant         = kv
    motor_lift.resistance             = res
    motor_lift.no_load_current        = io    
    motor_lift.gear_ratio             = 1.0
    motor_lift.gearbox_efficiency     = 1.0
    motor_lift.propeller_radius       = prop_lift.tip_radius
    net.motor_lift                    = motor_lift

    # append motor origin spanwise locations onto wing data structure 
    vehicle.append_component(net)
    
    #----------------------------------------------------------------------------------------
    # Add extra drag sources from motors, props, and landing gear. All of these hand measured
    #----------------------------------------------------------------------------------------
    motor_height                            = .25 * Units.feet
    motor_width                             =  1.6 * Units.feet    
    propeller_width                         = 1. * Units.inches
    propeller_height                        = propeller_width *.12    
    main_gear_width                         = 1.5 * Units.inches
    main_gear_length                        = 2.5 * Units.feet    
    nose_gear_width                         = 2. * Units.inches
    nose_gear_length                        = 2. * Units.feet    
    nose_tire_height                        = (0.7 + 0.4) * Units.feet
    nose_tire_width                         = 0.4 * Units.feet    
    main_tire_height                        = (0.75 + 0.5) * Units.feet
    main_tire_width                         = 4. * Units.inches    
    total_excrescence_area_spin             = 12.*motor_height*motor_width + \
        2.*main_gear_length*main_gear_width + nose_gear_width*nose_gear_length + \
        2*main_tire_height*main_tire_width + nose_tire_height*nose_tire_width
    
    total_excrescence_area_no_spin          = total_excrescence_area_spin + 12*propeller_height*propeller_width 
                                           
    vehicle.excrescence_area_no_spin        = total_excrescence_area_no_spin 
    vehicle.excrescence_area_spin           = total_excrescence_area_spin 
    
    vehicle.wings['main_wing'].motor_spanwise_locations = np.multiply(
        2./36.25,
        [-5.435, -5.435, -9.891, -9.891, -14.157, -14.157,
         5.435, 5.435, 9.891, 9.891, 14.157, 14.157])

    vehicle.wings['main_wing'].winglet_fraction = 0.0

    vehicle.wings['main_wing'].thickness_to_chord = 0.18
    vehicle.wings['main_wing'].chords.mean_aerodynamic = 0.9644599977664836
    
    #----------------------------------------------------------------------------------------
    # EVALUATE WEIGHTS using calculation (battery not updated) 
    #----------------------------------------------------------------------------------------
    #vehicle.weight_breakdown                = empty(vehicle)
    #MTOW                                    = vehicle.weight_breakdown.total
    #Payload                                 = vehicle.weight_breakdown.payload
    #OE                                      = MTOW - vehicle.weight_breakdown.battery               
    #vehicle.mass_properties.takeoff         = MTOW
    #vehicle.mass_properties.operating_empty = OE  
    
    
    return vehicle

def configs_setup(vehicle):


    # ------------------------------------------------------------------
    #   Initialize Configurations
    # ------------------------------------------------------------------

    configs = SUAVE.Components.Configs.Config.Container()

    base_config = SUAVE.Components.Configs.Config(vehicle)
    base_config.tag = 'base'
    configs.append(base_config)

    return configs
 