APPS.SingleWindowApp SingleWindowApp<NEdisplayMode="maximized"> {
   MODS.Read_Field readfield {
      read_field_ui {
         filename = ".\\bandedges_2d_2DEG.fld";
         portable = 0;
      };
   };
   MODS.extract_component select {
      in_field => <-.readfield.field;
   };
   MODS.surf_plot output {
      in_field => <-.select.out_fld;
   };
   GEOMS.Axis3D axis {
      in_field => <-.output.out_fld;
      x_axis_param {
         axis_name = "x[nm]";
      };
      y_axis_param {
         axis_name = "y[nm]";
      };
      z_axis_param {
         axis_name = "Energy[eV]";
      };
   };
   GEOMS.TextTitle title {
      TextUI {
         String {
            text = "Band structure, z[nm] = -106.0";
         };
      };
   };
   GDM.Uviewer3D viewer {
      Scene {
         Top {
            child_objs => {
               <-.<-.<-.output.out_obj,
               <-.<-.<-.axis.out_obj,
               <-.<-.<-.title.DefaultObject
            };
         };
      };
   };
};
