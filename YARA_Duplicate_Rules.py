#This script can identify and remove duplicate rules (based on rule name) from YARA files contained within a directory.
#Duplicate rules are logged to duplicate.log in the current directory.
#Rule names are echoed to standard out.
#Be sure to backup your data before using the remove option.

#Copyright (c) 2016 Ryan Boyle randomrhythm@rhythmengineering.com.
#All rights reserved.

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
from optparse import OptionParser
import sys
import datetime

def build_cli_parser():
    parser = OptionParser(usage="%prog [options]", description="Find duplicate YARA rules in a directory")
    parser.add_option("-r", "--remove", help="Remove duplicate rules", action="store_true")
    parser.add_option("-d", "--directory", action="store", default=None, dest="YARA_Directory_Path",
                      help="Folder path to directory containing YARA files")
    return parser
    
def ProcessRule(lstRuleFile, strYARApath):
  strYARAout = ""
  strLogOut = ""
  boolExcludeLine = False
  boolOverwrite = False
  for strRuleLine in lstRuleFile:
    if strRuleLine[:5] == "rule ":
      strRuleName = strRuleLine[-(len(strRuleLine) -5):]
      strRuleName = strRuleName[:len(strRuleName) -1]
      if strRuleName[-1:] == "\r":
        strRuleName = strRuleName[:-1]
      if strRuleName[-1:] == "{":
        strRuleName = strRuleName[:-1]
      if strRuleName[-1:] == " ":
        while strRuleName[-1:] == " ":
          strRuleName = strRuleName[:-1]        
      print strRuleName
      if strRuleName in dictRuleName:
        #print "duplicate rule in file " + strYARApath + " : " + strRuleName
        boolExcludeLine = True
        strLogOut = strLogOut + "Duplicate rule " + "\n" + strRuleName + " in " + dictRuleName[strRuleName]  + "\n" + strRuleName + " in " + strYARApath + "\n"
        if boolRemoveDuplicate == True:
          boolOverwrite = True
          strLogOut = strLogOut + "Removed rule " + strRuleName + " from " + strYARApath + "\n"
      else:
        dictRuleName[strRuleName] = strYARApath
        strYARAout = strYARAout + strRuleLine
        boolExcludeLine = False
    elif boolExcludeLine == False:
      strYARAout = strYARAout + strRuleLine
  if boolOverwrite == True:
    logToFile(strYARApath,strYARAout, True, "w")
  if len(strLogOut) > 1:
    strLogOut = "-------------" + "\n" + strLogOut  
  logToFile(strCurrentDirectory + "/duplicate.log",strLogOut, False, "a")
  
def logToFile(strfilePathOut, strDataToLog, boolDeleteFile, strWriteMode):
    target = open(strfilePathOut, strWriteMode)
    if boolDeleteFile == True:
      target.truncate()
    target.write(strDataToLog)
    target.close()

boolRemoveDuplicate = False
strCurrentDirectory = os.getcwd()
strYARADirectory = os.getcwd()
parser = build_cli_parser()
opts, args = parser.parse_args(sys.argv[1:])
if opts.remove:
  boolRemoveDuplicate = True
if opts.YARA_Directory_Path:
  strYARADirectory = opts.YARA_Directory_Path
dictRuleName = dict()
print strYARADirectory
logToFile(strCurrentDirectory + "/duplicate.log","Started " + str(datetime.datetime.now()) + "\n", False, "a")
for i in os.listdir(strYARADirectory):
  if i.endswith(".yar") or i.endswith(".yara"): 
      ##print i
      with open(strYARADirectory + '/' + i) as f:
        lines = f.readlines()
        ProcessRule(lines, strYARADirectory + '/' + i)
      continue
  else:
      continue
logToFile(strCurrentDirectory + "/duplicate.log","Completed " + str(datetime.datetime.now()) + "\n", False, "a")        
        

