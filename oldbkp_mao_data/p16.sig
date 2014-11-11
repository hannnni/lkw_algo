<?xml version="1.0" encoding="UTF-8"?>
<sc id="6" name="" frequency="1" steps="0" defaultIntergreenMatrix="0">
  <sgs>
    <sg id="1" name="Signalgruppe 1" defaultSignalSequence="3">
      <defaultDurations />
    </sg>
    <sg id="2" name="Signalgruppe 2" defaultSignalSequence="3">
      <defaultDurations />
    </sg>
    <sg id="3" name="Signalgruppe 3" defaultSignalSequence="3">
      <defaultDurations />
    </sg>
  </sgs>
  <intergreenmatrices />
  <progs>
    <prog id="1" cycletime="70000" switchpoint="0" offset="0" intergreens="0" fitness="0.000000" vehicleCount="0" name="Signalprogramm 1">
      <sgs>
        <sg sg_id="1" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="20000" />
            <cmd display="1" begin="40000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="2" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="19000" />
            <cmd display="1" begin="37000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="3" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="15000" />
            <cmd display="3" begin="42000" />
          </cmds>
          <fixedstates>
            <fixedstate display="4" duration="3000" />
            <fixedstate display="2" duration="1000" />
          </fixedstates>
        </sg>
      </sgs>
    </prog>
  </progs>
  <stages />
  <interstageProgs />
  <stageProgs />
  <dailyProgLists />
</sc>