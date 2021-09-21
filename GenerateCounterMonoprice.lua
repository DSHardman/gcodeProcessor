radius = 15
height = 5

-- emit a shape
shape = ccylinder(radius, height)
emit(shape)

--###########################################################

-- setting up printer settings
set_setting_value('printer', 'Monoprice_select_mini_v2')
set_setting_value('z_layer_height_mm', 0.2)

-- setting up some slicing settings
set_setting_value('infill_type_0', 'Phasor')
set_setting_value('num_shells_0', 0)
set_setting_value('cover_thickness_mm_0', 0.0)
set_setting_value('print_perimeter_0', false)
set_setting_value('infill_percentage_0',20)

-- printing settings (for TPU, on CR-10 with Titan or Hemera direct extruder)
set_setting_value('filament_priming_mm_0',0.0)
set_setting_value('extruder_temp_degree_c_0',210.0)

set_setting_value('nozzle_diameter_mm_0',0.8)

set_setting_value('flow_multiplier_0',1)
set_setting_value('speed_multiplier_0',1)
set_setting_value('filament_priming_mm_0',0)

--###########################################################

-- allocating  the field as 3D textures
-- as of today all fields have to be 64x64x64
phi = tex3d_rgb8f(64,64,64)
iso = tex3d_rgb8f(64,64,64)

-- filling the 3D textures
-- values in 3D textures are always in [0,1]
-- the textures can hold up to three components
for i = 0,63 do
  for j = 0,63 do
    for k = 0,63 do
      -- sphere center
      x = i - 40
      y = j - 40
      z = k - 85
      b = (atan2(z,y) / 360  + 0.5  +0.25 )%1.0
      phi:set(i,j,k, v(b,b,b))
      -- isotropy
      if length(v(x,y,z)) < 70 then
        iso:set(i,j,k, v(0,0,0))
      else
        iso:set(i,j,k, v(0.5,0.5,0.5))
      end
    end
  end
end

-- binding the 3D textures to the fields
-- the binding requires a field (!), a bounding box where it is applied, and the internal name of the parameter (see tooltip in UI)
set_setting_value('phasor_infill_iso_0', iso, v(-radius,-radius,-height/2), v(radius,radius,height/2))
set_setting_value('phasor_infill_theta_0', 0)
set_setting_value('phasor_infill_phi_0', phi, v(-radius,-radius,-height/2), v(radius,radius,height/2))
