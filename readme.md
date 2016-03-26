mantOS
======

What is MANTA Project
---------------------

MANTA is a project which aims to develop a marine autonomous drone for cartography in shallow waters. This drone should be able to locate itself precisely using an IMU and a GPS. For more precise data, IMU/GPS fusion has been explored, without any probing results.

Technology and implementation
-----------------------------

Motors are controlled by an Arduino Uno and 2 ESC (Electronic Speed Controller), one for each motor.

We used ROS on a Raspberry Pi 2 for the implementation and the gathering of data from all the sensors which are respectively :

- IMU
- GPS
- Echo-sounder
- Laser rangefinder

Results
-------

The ouput file allowed us to see the map of depths and to extrapolate missing data using Matlab packages. Yo can see bellow one example of the experimentation we conduce on a lac near our school.

![alt tag](https://raw.githubusercontent.com/epsichaos/mantos/master/img/map.png)
