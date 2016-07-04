#!/usr/bin/lua
local oldpowera=0
local oldpowerb=0
local mem=manager:machine().devices[":maincpu"].spaces["program"]
local game=emu.romname()

local function speak(text)
    io.popen("espeak".." \""..text.."\"")
end

local function shock(channel,action)
    p = io.popen("python3 etgame.py "..channel.." "..action)
end

--[[ SF2: ff83f0 an ff86f0 are words container current power bar level of sf2
     0 = not in a game.  144 = max.  Then it drops as you get hit, never
     to 0, -1 when KO'd
     there are lots of sf2 variants, probably you need the specific sha1sum:
     bd59872a57f14dc492e2fb387727a9402f3d4f97  sf2.zip
--]]

local function checksf2power()
         local powera = mem:read_i16(0xff83f0)
         if (powera ~= oldpowera) then
            if (powera == -1) then
               shock("-c a","-l 255")
             elseif (powera == 0) then
               shock("","-l 0")    -- End of Game
            elseif (powera > oldpowera) then
               shock("","-l 0")    -- Start of Game
            else
               shock("-c a","-r 250")                        
            end
            oldpowera = powera
         end

         local powerb = mem:read_i16(0xff86f0)
         if (powerb ~= oldpowerb) then
            if (powerb == -1) then
               shock("-c b","-l 255")
            elseif (powerb < oldpowerb) then
               shock("-c b","-r 250")                        
            end
            oldpowerb = powerb
         end
end

shock("","-l 0")
if (game == "sf2") then
   emu.sethook(checksf2power,"frame")
else
   print("No shocks for this game")
end
