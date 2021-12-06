EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Connector:Conn_01x08_Male J1
U 1 1 61827B08
P 3350 3550
F 0 "J1" H 3322 3524 50  0000 R CNN
F 1 "Conn_01x08_Male" H 3322 3433 50  0000 R CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x08_P2.54mm_Vertical" H 3350 3550 50  0001 C CNN
F 3 "~" H 3350 3550 50  0001 C CNN
	1    3350 3550
	-1   0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x02_Female J_LED12V1
U 1 1 6182CB03
P 5850 3050
F 0 "J_LED12V1" H 5878 3026 50  0000 L CNN
F 1 "Conn_01x02_Female" H 5878 2935 50  0000 L CNN
F 2 "TerminalBlock:TerminalBlock_bornier-2_P5.08mm" H 5850 3050 50  0001 C CNN
F 3 "~" H 5850 3050 50  0001 C CNN
	1    5850 3050
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x02_Female J_LED_izlaz1
U 1 1 6182D9C0
P 5850 3500
F 0 "J_LED_izlaz1" H 5878 3476 50  0000 L CNN
F 1 "Conn_01x02_Female" H 5878 3385 50  0000 L CNN
F 2 "TerminalBlock:TerminalBlock_bornier-2_P5.08mm" H 5850 3500 50  0001 C CNN
F 3 "~" H 5850 3500 50  0001 C CNN
	1    5850 3500
	1    0    0    -1  
$EndComp
$Comp
L Transistor_FET:IRLIZ44N MOSFET
U 1 1 6182EA81
P 4050 2250
F 0 "MOSFET" H 4255 2296 50  0000 L CNN
F 1 "IRLIZ44N" H 4255 2205 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-220F-3_Vertical" H 4300 2175 50  0001 L CIN
F 3 "http://www.irf.com/product-info/datasheets/data/irliz44n.pdf" H 4050 2250 50  0001 L CNN
	1    4050 2250
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x02_Male Jumper_setup
U 1 1 6182FEAF
P 5300 2450
F 0 "Jumper_setup" H 5408 2631 50  0000 C CNN
F 1 "Conn_01x02_Male" H 5408 2540 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" H 5300 2450 50  0001 C CNN
F 3 "~" H 5300 2450 50  0001 C CNN
	1    5300 2450
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x08_Male J2
U 1 1 6182AE06
P 4400 3550
F 0 "J2" H 4508 4031 50  0000 C CNN
F 1 "Conn_01x08_Male" H 4508 3940 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x08_P2.54mm_Vertical" H 4400 3550 50  0001 C CNN
F 3 "~" H 4400 3550 50  0001 C CNN
	1    4400 3550
	1    0    0    -1  
$EndComp
$Comp
L Device:R R_mosfet
U 1 1 61833B0B
P 3700 2250
F 0 "R_mosfet" V 3493 2250 50  0000 C CNN
F 1 "R" V 3584 2250 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 3630 2250 50  0001 C CNN
F 3 "~" H 3700 2250 50  0001 C CNN
	1    3700 2250
	0    1    1    0   
$EndComp
Text GLabel 3550 2250 0    50   Input ~ 0
P4
Text GLabel 3150 3350 0    50   Input ~ 0
P4
Text GLabel 4600 3550 2    50   Input ~ 0
P9
Text GLabel 5500 2450 2    50   Input ~ 0
P9
Text GLabel 4600 3950 2    50   Input ~ 0
GND
Text GLabel 5650 3150 0    50   Input ~ 0
GND
Text GLabel 5500 2550 2    50   Input ~ 0
GND
NoConn ~ 3150 3250
NoConn ~ 3150 3450
NoConn ~ 3150 3850
NoConn ~ 4600 3750
NoConn ~ 4600 3650
NoConn ~ 4600 3250
NoConn ~ 4600 3350
NoConn ~ 4600 3450
$Comp
L Device:R R_mosfet1kohm
U 1 1 61836211
P 3900 2400
F 0 "R_mosfet1kohm" H 3830 2354 50  0000 R CNN
F 1 "R" H 3830 2445 50  0000 R CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 3830 2400 50  0001 C CNN
F 3 "~" H 3900 2400 50  0001 C CNN
	1    3900 2400
	-1   0    0    1   
$EndComp
Text GLabel 3900 2550 3    50   Input ~ 0
GND
$Comp
L Connector:Conn_01x03_Female Juart
U 1 1 61836FCD
P 2450 2550
F 0 "Juart" H 2478 2576 50  0000 L CNN
F 1 "Conn_01x03_Female" H 2478 2485 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 2450 2550 50  0001 C CNN
F 3 "~" H 2450 2550 50  0001 C CNN
	1    2450 2550
	1    0    0    -1  
$EndComp
Text GLabel 3150 3650 0    50   Input ~ 0
tx
Text GLabel 2250 2450 0    50   Input ~ 0
tx
Text GLabel 2250 2550 0    50   Input ~ 0
rx
Text GLabel 3150 3750 0    50   Input ~ 0
rx
Text GLabel 2250 2650 0    50   Input ~ 0
GND
NoConn ~ 3150 3550
NoConn ~ 3150 3950
$Comp
L Connector:Conn_01x02_Female inpput_5v
U 1 1 61838A38
P 5900 4000
F 0 "inpput_5v" H 5928 3976 50  0000 L CNN
F 1 "Conn_01x02_Female" H 5928 3885 50  0000 L CNN
F 2 "TerminalBlock:TerminalBlock_bornier-2_P5.08mm" H 5900 4000 50  0001 C CNN
F 3 "~" H 5900 4000 50  0001 C CNN
	1    5900 4000
	1    0    0    -1  
$EndComp
Text GLabel 5700 4100 0    50   Input ~ 0
GND
Text GLabel 5700 4000 0    50   Input ~ 0
5vin
Text GLabel 4600 3850 2    50   Input ~ 0
5vin
Text GLabel 4150 2450 2    50   Input ~ 0
GND
Text GLabel 4150 2050 2    50   Input ~ 0
DRAIN
Text GLabel 5650 3050 0    50   Input ~ 0
12V+
Text GLabel 5650 3600 0    50   Input ~ 0
DRAIN
Text GLabel 5650 3500 0    50   Input ~ 0
12V+
$EndSCHEMATC
