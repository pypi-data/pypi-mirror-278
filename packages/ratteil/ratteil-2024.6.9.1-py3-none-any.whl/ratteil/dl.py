import os, ratteil.base as base
from pathlib import Path
def dl(streamer, max_len, surahs_list, recitersDB, resourcesPath, validation=False, previous_len=None):
  """
    Download audios files
  """
  MAX_ST = False
  current_len = 0 
  ensure_max = []
  if previous_len:
    current_len = previous_len
  
  DOWNLOAD_PATH = Path(f"{resourcesPath}/audios")
  if not validation: # avoid deleting audios on validation process 
    OLD_FILES = base.g.glob(f"{DOWNLOAD_PATH}/*")
    if len(OLD_FILES) >= 1:
      for file in OLD_FILES:
        y = file.split("/")[-1]
        z = "audios/%s" % y
        if z not in surahs_list:
          os.remove(file)
        else:
          surahs_list.remove(z)
          file_len = streamer.get_length(file)
          current_len += file_len
          ensure_max.append({
            "file": file,
            "file_len": file_len,
            "less10": file_len < 10
          })

  for x in surahs_list:
    surah = base.SurahInfo(*base.filename_resolve(x), recitersDB)
    SURAH_PATH = DOWNLOAD_PATH / surah.dl_name
    #os.system("clear")
    URL = f"{surah.url}{base.surah_index_to_filename(surah.id)}"
    if not SURAH_PATH.exists():
      if current_len < max_len:
        os.system(f"wget {URL}  -O {SURAH_PATH}")
        file_len = streamer.get_length(SURAH_PATH)
        current_len += file_len
        ensure_max.append({
          "file": SURAH_PATH,
          "file_len": file_len,
          "less10": file_len < 10
        })
      else:
        MAX_ST = True
  
  #current length to max_length reminder
  cur_mx_rem = abs(current_len - max_len)
  if cur_mx_rem > 1:
    for y in range(1,3):
      for i in ensure_max:
        xyz = abs(current_len - i["file_len"])
        if xyz >= (max_len+3) or (xyz >= max_len+1 and xyz <= (max_len+1)):
          current_len -= i["file_len"]
          os.remove(i["file"])
          ensure_max.remove(i)
    print("current : ", current_len) 
       
  return current_len, MAX_ST