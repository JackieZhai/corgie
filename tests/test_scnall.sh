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


corgie downsample \
--src_layer_spec '{
   "path": "file:///dc0/CodeReAlign/corgie/tests/img/unaligned"
   }' \
--mip_start 0 --mip_end 2 \
--start_coord "5000, 5000, 5990" \
--end_coord "15000, 15000, 6010" \
--chunk_xy 2000


corgie normalize \
--src_layer_spec '{
   "path": "file:///dc0/CodeReAlign/corgie/tests/img/unaligned",
      "name": "img"
      }' \
--dst_folder file:///dc0/CodeReAlign/corgie/tests \
--stats_mip 1 --mip_start 0 --mip_end 2 \
--start_coord "5000, 5000, 5990" \
--end_coord "15000, 15000, 6010" \
--chunk_xy 2000 \
--suffix norm


corgie align-block \
--src_layer_spec '{"path": "file:///dc0/CodeReAlign/corgie/tests/img/unaligned"}' \
--dst_folder file:///dc0/CodeReAlign/corgie/tests/aligned_blockmatch \
--start_coord "100000, 100000, 17000" \
--start_coord "5000, 5000, 5990" \
--end_coord "15000, 15000, 6010" \
--chunk_xy 2000 \
--render_chunk_xy 2000 \
--suffix run_x1 \
--processor_spec '{"ApplyModel": {
   "params": {
      "path": "https://storage.googleapis.com/corgie_package/models/aligners/blockmatch",
      "tile_size": 100,
      "tile_step": 50,
      "max_disp": 48,
      "r_delta": 1.3
  }}}' \
--processor_mip 1


corgie align-block \
--src_layer_spec '{"path": "file:///dc0/CodeReAlign/corgie/tests/img/img_norm"}' \
--dst_folder file:///dc0/CodeReAlign/corgie/tests/aligned_seamless \
--start_coord "5000, 5000, 5990" \
--end_coord "15000, 15000, 6010" \
--chunk_xy 2000 \
--render_chunk_xy 2000 \
--processor_spec '{"ApplyModel": {
   "params": {"path": "https://storage.googleapis.com/corgie_package/models/aligners/MICrONS_aligner_512_1024nm"}
}}' \
--processor_mip 1 \
--device cuda \
--suffix aligned