<?xml version="1.0" encoding="UTF-8"?>
<sc id="10" name="" frequency="1" steps="0" defaultIntergreenMatrix="0">
  <sgs>
    <sg id="1" name="DR" defaultSignalSequence="3">
      <defaultDurations />
    </sg>
    <sg id="2" name="DL" defaultSignalSequence="3">
      <defaultDurations />
    </sg>
    <sg id="3" name="B" defaultSignalSequence="3">
      <defaultDurations />
    </sg>
    <sg id="4" name="A" defaultSignalSequence="3">
      <defaultDurations />
    </sg>
  </sgs>
  <intergreenmatrices />
  <progs>
    <prog id="1" cycletime="70000" switchpoint="0" offset="0" intergreens="0" fitness="0.000000" vehicleCount="0" name="Signalprogramm 1">
      <sgs>
        <sg sg_id="1" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="4000" />
            <cmd display="1" begin="18000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="2" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="16000" />
            <cmd display="1" begin="33000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="3" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="40000" />
            <cmd display="1" begin="69000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="4" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="14000" />
            <cmd display="3" begin="37000" />
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