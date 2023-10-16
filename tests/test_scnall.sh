corgie copy \
--src_layer_spec '{
   "name": "unaligned",
   "path": "file:///dc50TB/Neuroglancer/scnall_raw_scr"
   }' \
--dst_folder file:///dc0/CodeReAlign/corgie/tests \
--mip 0 \
--start_coord "5000, 5000, 5990" \
--end_coord "15000, 15000, 6010" \
--chunk_xy 2000 --chunk_z 1
