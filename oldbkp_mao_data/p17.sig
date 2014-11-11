<?xml version="1.0" encoding="UTF-8"?>
<sc id="7" name="" frequency="1" steps="0" defaultIntergreenMatrix="0">
  <sgs>
    <sg id="1" name="C" defaultSignalSequence="3">
      <defaultDurations />
    </sg>
    <sg id="2" name="B" defaultSignalSequence="3">
      <defaultDurations />
    </sg>
    <sg id="3" name="DL" defaultSignalSequence="3">
      <defaultDurations />
    </sg>
    <sg id="4" name="D" defaultSignalSequence="3">
      <defaultDurations />
    </sg>
    <sg id="5" name="A" defaultSignalSequence="3">
      <defaultDurations />
    </sg>
  </sgs>
  <intergreenmatrices />
  <progs>
    <prog id="1" cycletime="70000" switchpoint="0" offset="0" intergreens="0" fitness="0.000000" vehicleCount="0" name="Signalprogramm 1">
      <sgs>
        <sg sg_id="1" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="7000" />
            <cmd display="1" begin="38000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="2" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="42000" />
            <cmd display="1" begin="58000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="3" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="3000" />
            <cmd display="3" begin="62000" />
          </cmds>
          <fixedstates>
            <fixedstate display="4" duration="3000" />
            <fixedstate display="2" duration="1000" />
          </fixedstates>
        </sg>
        <sg sg_id="4" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="40000" />
            <cmd display="3" begin="65000" />
          </cmds>
          <fixedstates>
            <fixedstate display="4" duration="3000" />
            <fixedstate display="2" duration="1000" />
          </fixedstates>
        </sg>
        <sg sg_id="5" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="43000" />
            <cmd display="1" begin="59000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
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