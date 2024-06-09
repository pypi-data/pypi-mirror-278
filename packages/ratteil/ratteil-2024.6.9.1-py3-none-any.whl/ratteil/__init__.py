"""
RatTeil is a app to live stream the Holly Quran to youtube
Copyright (C) 2024  Ali Elfatih

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
def ratteil():
  import os, time, ratteil.base as base, random as r, ratteil.dl as dl, glob as g
  import argparse
  from ratteil.base import RatTeil
  from pathlib import Path
  from ratteil.reciters import reciters_code as recitersCodesDB, reciters as recitersDB
  
  ####
  
  USER_HOME = Path.home()
  RATTEIL_RESOURCES= USER_HOME / "RatTeil-resources"
  RATTEIL_PATH = Path(__file__).parents[0]
  
  if not RATTEIL_RESOURCES.exists():
    #first time setup
    RATTEIL_RESOURCES.mkdir()
    os.mkdir(f"{RATTEIL_RESOURCES}/audios")
    os.mkdir(f"{RATTEIL_RESOURCES}/imgs")
    os.mkdir(f"{RATTEIL_RESOURCES}/fixer")
    os.mkdir(f"{RATTEIL_RESOURCES}/fb_stream")
    os.system(f"cp -r {RATTEIL_PATH}/fixer/* {RATTEIL_RESOURCES}/fixer/")
    os.system(f"cp -r {RATTEIL_PATH}/imgs/* {RATTEIL_RESOURCES}/imgs/")
  
  def PRE_LUNCHER(options, RATTEIL_RESOURCES):
    streamer = RatTeil(recitersDB, recitersCodesDB, RATTEIL_RESOURCES, RATTEIL_PATH)
    temp_reciters_list=[]
    streamer.surah_index = options.surah
    if options.reciter:
      options.reciters_number == len(options.reciter)
      temp_reciters_list = options.reciter 
    else:
      temp_reciters_list = recitersCodesDB
    
    if not options.no_download:
      streamer.generate_random_reciters_list(options.reciters_number, temp_reciters_list)
      #test and improve needed 
      streamer.generate_random_surahs_list(options.surahs_number, options.surah)
      
      previous_len, max_st = dl.dl(streamer, options.max_len, streamer.stream_surahs_list, streamer.recitersDB, streamer.resourcesPath)
      
      if not options.no_validation:
        minimum_stream_length = 0 
        if options.stream_numbers:
          minimum_stream_length = options.stream_numbers * 75.0
        elif options.surahs_number:
          minimum_stream_length = 0
        else:
          minimum_stream_length = options.minimum_stream_length 
          if not max_st:
            aea = base.stream_validation(streamer, options.max_len, g.glob(f"{streamer.resourcesPath}/audios/*"), minimum_stream_length,temp_reciters_list, previous_len)
    
    
    luncher(streamer, sites=options.sites)
  
  def luncher(streamer, sites):
    streamer.prepare_stream_files(g.glob(f"{streamer.resourcesPath}/audios/*"))
    
    for stream in streamer.streams:
      streamer.generate_stream_details(stream)
      streamer.stream(stream, sites)
      time.sleep(60)  


  parser = argparse.ArgumentParser(prog="RatTeil",
  description="Stream The Holly Quran to a youtube channel.", 
  epilog="""
    RatTeil  Copyright (C) 2024  Ali Elfatih. \n
  This program comes with ABSOLUTELY NO WARRANTY. \n
  This is free software, and you are welcome to redistribute it under certain conditions; \n \t type `ratteil -c' for details.
    Made with ♡ & ^_^ by Moddaker Team""",
  formatter_class=argparse.ArgumentDefaultsHelpFormatter
  )
  parser.add_argument("-c", "--copyright", help="Show Copyright LICENSE.",action="store_const",const=True, dest="copyright")
  parser.add_argument("-l","--list", metavar="", help="available reciters", action="store_const", const=True, default=False, dest="reciters_list")
  parser.add_argument("-mx", "--max", metavar="",help="max stream length in minutes", type=float, default=450, dest="max_len")
  parser.add_argument("-m","--min", metavar="", type=float, help="minimum streams length in minutes", default=120.0, dest="minimum_stream_length")
  parser.add_argument("-ms","--streams",metavar="", type=float, help="minimum streams number. Note that each stream'll be 75 minute or less", dest="stream_numbers")
  parser.add_argument("-n", metavar="", type=int, help="number of reciters per stream", default=r.randrange(3,7), dest="reciters_number")
  parser.add_argument("-R","--reciter", metavar="", help="choose reciter or reciters by code", dest="reciter", nargs="*", choices=recitersCodesDB)
  parser.add_argument("-r", "--resume",metavar="", help="resume previous stream", action="store_const", const=True, default=False, dest="resume_stream")
  parser.add_argument("-sn", metavar="", type=int, help="Surahs number per stream", default=r.randrange(20,50), dest="surahs_number")
  parser.add_argument("-s","--surah", metavar="", type=int,choices=[i for i in range(1,115)] ,help="choose surah by index", dest="surah")
  parser.add_argument("--no-download", metavar="", default=False, help="stream existing files; no new downloads", dest="no_download", action='store_const', const=True)
  parser.add_argument("--no-validation", metavar="", help="stop minimum streams validation", default=False, action="store_const", const=True, dest="no_validation")
  parser.add_argument("-t","--sites", metavar="", help="site to stream to", dest="sites", choices=["youtube","yt","fb","facebook"], nargs="*")
  parser.add_argument("-d", "--dev",dest="dev", action="store_const", const=True)
  

  args = parser.parse_args()
  if args.dev:
    from ratteil.base_test import recs as recitersDB
    
  if ((not args.sites) and (not args.reciters_list)) and (not args.copyright):
    os.system("clear")
    print("!! sites are required at least one site !! \n")
    print("ex:\n $ ratteil -t youtube \n")
    
    exit(0)
    
  if args.reciters_list:
    streamer = RatTeil(recitersDB,recitersCodesDB, RATTEIL_RESOURCES,RATTEIL_PATH)
    reciters_list = streamer.get_available_reciters_list()
    reciters_list.sort()
    for reciter in reciters_list:
      print(reciter)
      
    print("""
      RatTeil is a app to live stream the Holly Quran to youtube
      Copyright (C) 2024  Ali Elfatih
      
      This program is free software: you can redistribute it and/or modify
      it under the terms of the GNU General Public License as published by
      the Free Software Foundation, either version 3 of the License, or any later version.
      
      This program is distributed in the hope that it will be useful,
      but WITHOUT ANY WARRANTY; without even the implied warranty of
      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
      GNU General Public License for more details.
      
      You should have received a copy of the GNU General Public License
      along with this program.  If not, see <https://www.gnu.org/licenses/>.
      """)
  elif args.copyright:
    copyright_file = open(RATTEIL_PATH / "LICENSE", "r")
    for line in copyright_file:
      print(line)
    exit(0)
  else:
    PRE_LUNCHER(args, RATTEIL_RESOURCES)
