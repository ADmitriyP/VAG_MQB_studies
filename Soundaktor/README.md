<p align="center">
    <img src="https://github.com/ADmitriyP/VAG_MQB_studies/blob/main/Soundaktor/VIEW.jpg" alt="logo" style="width:50%; height:auto;"/>
</p>
<p></p>This script is designed for the convenience of viewing SoundActor GEN 2.0 firmware data on the portal http://www.mqbtools.nl/soundaktor/.</p>

<p>This Python script performs a recursive traversal of files in the current directory that contain SoundActor firmware files (SAK). It subsequently extracts the DATA_02 data block, converts the data from HEX to ASCII, and saves the resulting file in a separate DATA_02 directory.</p>