<?xml version="1.0" encoding="UTF-8"?>
<sc id="2" name="" frequency="1" steps="0" defaultIntergreenMatrix="0">
  <sgs>
    <sg id="1" name="Signalgruppe 1" defaultSignalSequence="3">
      <notes>west to east , go strait and turing</notes>
      <defaultDurations />
    </sg>
    <sg id="2" name="Signalgruppe 2" defaultSignalSequence="3">
      <notes>minor road</notes>
      <defaultDurations />
    </sg>
  </sgs>
  <intergreenmatrices>
    <intergreenmatrix id="1" name="Zwischenzeitmatrix 1">
      <intergreen clearingsg="2" enteringsg="1" value="6000" />
      <intergreen clearingsg="1" enteringsg="2" value="6000" />
    </intergreenmatrix>
  </intergreenmatrices>
  <progs>
    <prog id="1" cycletime="60000" switchpoint="0" offset="0" intergreens="0" fitness="0.000000" vehicleCount="0" name="Signalprogramm 1">
      <sgs>
        <sg sg_id="1" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="2000" />
            <cmd display="1" begin="33000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="2" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="36000" />
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