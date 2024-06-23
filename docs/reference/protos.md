# Protocol Documentation
<a name="top"></a>

## Table of Contents

- [circuit.proto](#circuit-proto)
    - [Concat](#vlsir-circuit-Concat)
    - [Connection](#vlsir-circuit-Connection)
    - [ConnectionTarget](#vlsir-circuit-ConnectionTarget)
    - [ExternalModule](#vlsir-circuit-ExternalModule)
    - [Instance](#vlsir-circuit-Instance)
    - [Interface](#vlsir-circuit-Interface)
    - [Module](#vlsir-circuit-Module)
    - [Package](#vlsir-circuit-Package)
    - [Port](#vlsir-circuit-Port)
    - [Signal](#vlsir-circuit-Signal)
    - [Slice](#vlsir-circuit-Slice)
  
    - [Port.Direction](#vlsir-circuit-Port-Direction)
    - [SpiceType](#vlsir-circuit-SpiceType)
  
- [netlist.proto](#netlist-proto)
    - [NetlistInput](#vlsir-netlist-NetlistInput)
    - [NetlistResult](#vlsir-netlist-NetlistResult)
  
    - [NetlistFormat](#vlsir-netlist-NetlistFormat)
  
    - [Netlist](#vlsir-netlist-Netlist)
  
- [spice.proto](#spice-proto)
    - [AcInput](#vlsir-spice-AcInput)
    - [AcResult](#vlsir-spice-AcResult)
    - [AcResult.MeasurementsEntry](#vlsir-spice-AcResult-MeasurementsEntry)
    - [Analysis](#vlsir-spice-Analysis)
    - [AnalysisResult](#vlsir-spice-AnalysisResult)
    - [ComplexNum](#vlsir-spice-ComplexNum)
    - [Control](#vlsir-spice-Control)
    - [CustomAnalysisInput](#vlsir-spice-CustomAnalysisInput)
    - [CustomAnalysisResult](#vlsir-spice-CustomAnalysisResult)
    - [DcInput](#vlsir-spice-DcInput)
    - [DcResult](#vlsir-spice-DcResult)
    - [DcResult.MeasurementsEntry](#vlsir-spice-DcResult-MeasurementsEntry)
    - [Include](#vlsir-spice-Include)
    - [LibInclude](#vlsir-spice-LibInclude)
    - [LinearSweep](#vlsir-spice-LinearSweep)
    - [LogSweep](#vlsir-spice-LogSweep)
    - [Meas](#vlsir-spice-Meas)
    - [MonteInput](#vlsir-spice-MonteInput)
    - [MonteResult](#vlsir-spice-MonteResult)
    - [NoiseInput](#vlsir-spice-NoiseInput)
    - [NoiseResult](#vlsir-spice-NoiseResult)
    - [NoiseResult.IntegratedNoiseEntry](#vlsir-spice-NoiseResult-IntegratedNoiseEntry)
    - [NoiseResult.MeasurementsEntry](#vlsir-spice-NoiseResult-MeasurementsEntry)
    - [OpInput](#vlsir-spice-OpInput)
    - [OpResult](#vlsir-spice-OpResult)
    - [PointSweep](#vlsir-spice-PointSweep)
    - [Save](#vlsir-spice-Save)
    - [Signal](#vlsir-spice-Signal)
    - [SimInput](#vlsir-spice-SimInput)
    - [SimOptions](#vlsir-spice-SimOptions)
    - [SimResult](#vlsir-spice-SimResult)
    - [Sweep](#vlsir-spice-Sweep)
    - [SweepInput](#vlsir-spice-SweepInput)
    - [SweepResult](#vlsir-spice-SweepResult)
    - [TranInput](#vlsir-spice-TranInput)
    - [TranInput.IcEntry](#vlsir-spice-TranInput-IcEntry)
    - [TranResult](#vlsir-spice-TranResult)
    - [TranResult.MeasurementsEntry](#vlsir-spice-TranResult-MeasurementsEntry)
  
    - [Save.SaveMode](#vlsir-spice-Save-SaveMode)
    - [Signal.Quantity](#vlsir-spice-Signal-Quantity)
  
    - [Spice](#vlsir-spice-Spice)
  
- [tech.proto](#tech-proto)
    - [LayerInfo](#vlsir-tech-LayerInfo)
    - [LayerPurpose](#vlsir-tech-LayerPurpose)
    - [Package](#vlsir-tech-Package)
    - [Technology](#vlsir-tech-Technology)
  
    - [LayerPurposeType](#vlsir-tech-LayerPurposeType)
  
- [utils.proto](#utils-proto)
    - [AuthorMetadata](#vlsir-utils-AuthorMetadata)
    - [LibraryMetadata](#vlsir-utils-LibraryMetadata)
    - [Param](#vlsir-utils-Param)
    - [ParamValue](#vlsir-utils-ParamValue)
    - [Prefixed](#vlsir-utils-Prefixed)
    - [QualifiedName](#vlsir-utils-QualifiedName)
    - [Reference](#vlsir-utils-Reference)
  
    - [SIPrefix](#vlsir-utils-SIPrefix)
  
- [Scalar Value Types](#scalar-value-types)



<a name="circuit-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## circuit.proto



<a name="vlsir-circuit-Concat"></a>

### Concat
Signal Concatenation
FIXME: documentation of ordering, MSB-LSB


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| parts | [ConnectionTarget](#vlsir-circuit-ConnectionTarget) | repeated |  |






<a name="vlsir-circuit-Connection"></a>

### Connection
Port Connection 
Pairing between an Instance port (name) and a parent-module ConnectionTarget.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| portname | [string](#string) |  |  |
| target | [ConnectionTarget](#vlsir-circuit-ConnectionTarget) |  |  |






<a name="vlsir-circuit-ConnectionTarget"></a>

### ConnectionTarget
ConnectionTarget Union
Enumerates all types that can be
(a) Connected to Ports, and
(b) Concatenated


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| sig | [string](#string) |  | Reference to `Signal` (name) `sig` |
| slice | [Slice](#vlsir-circuit-Slice) |  | Slice into signals |
| concat | [Concat](#vlsir-circuit-Concat) |  | Concatenation of signals |






<a name="vlsir-circuit-ExternalModule"></a>

### ExternalModule
Externally Defined Module
Primarily for sake of port-ordering, for translation with connect-by-position
formats.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| name | [vlsir.utils.QualifiedName](#vlsir-utils-QualifiedName) |  | Qualified External Module Name |
| desc | [string](#string) |  | Description |
| ports | [Port](#vlsir-circuit-Port) | repeated | Port Definitions Ordered as they will be in order-sensitive formats, such as typical netlist formats. |
| signals | [Signal](#vlsir-circuit-Signal) | repeated | Signal Definitions, limited to those used by external-facing ports. |
| parameters | [vlsir.utils.Param](#vlsir-utils-Param) | repeated | Params |
| spicetype | [SpiceType](#vlsir-circuit-SpiceType) |  | Spice Type, SUBCKT by default |






<a name="vlsir-circuit-Instance"></a>

### Instance
Module Instance


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| name | [string](#string) |  | Instance Name |
| module | [vlsir.utils.Reference](#vlsir-utils-Reference) |  | Reference to Module instantiated |
| parameters | [vlsir.utils.Param](#vlsir-utils-Param) | repeated | Parameter Values |
| connections | [Connection](#vlsir-circuit-Connection) | repeated | Port `Connection`s |






<a name="vlsir-circuit-Interface"></a>

### Interface
Interface
Defines the logical IO of a `Module`


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| name | [string](#string) |  | Cell Name |
| ports | [Port](#vlsir-circuit-Port) | repeated | Port List |






<a name="vlsir-circuit-Module"></a>

### Module
Module - the primary unit of hardware re-use


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| name | [string](#string) |  | Module Name |
| ports | [Port](#vlsir-circuit-Port) | repeated | Port List, referring to elements of `signals` by name Ordered as they will be in order-sensitive formats, such as typical netlist formats. |
| signals | [Signal](#vlsir-circuit-Signal) | repeated | Signal Definitions, including externally-facing `Port` signals |
| instances | [Instance](#vlsir-circuit-Instance) | repeated | Module Instances |
| parameters | [vlsir.utils.Param](#vlsir-utils-Param) | repeated | Parameters |
| literals | [string](#string) | repeated | Literal Contents, e.g. in downstream EDA formats |






<a name="vlsir-circuit-Package"></a>

### Package
Package
A Collection of Modules and ExternalModules


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| domain | [string](#string) |  | Domain Name |
| modules | [Module](#vlsir-circuit-Module) | repeated | `Module` Definitions |
| ext_modules | [ExternalModule](#vlsir-circuit-ExternalModule) | repeated | `ExternalModule` interfaces used by `modules`, and available externally |
| desc | [string](#string) |  | Description |






<a name="vlsir-circuit-Port"></a>

### Port
Port
An externally-visible `Signal` with a `Direction`.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| signal | [string](#string) |  | Reference to `Signal` by name |
| direction | [Port.Direction](#vlsir-circuit-Port-Direction) |  | Port direction |






<a name="vlsir-circuit-Signal"></a>

### Signal
Signal
A named connection element, potentially with non-unit `width`.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| name | [string](#string) |  | Signal Name |
| width | [int64](#int64) |  | Bus Width |






<a name="vlsir-circuit-Slice"></a>

### Slice
Signal Slice
Reference to a subset of bits of `signal`.
Indices `top` and `bot` are both inclusive, similar to popular HDLs.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| signal | [string](#string) |  | Parent Signal Name |
| top | [int64](#int64) |  | Top Index |
| bot | [int64](#int64) |  | Bottom Index |





 


<a name="vlsir-circuit-Port-Direction"></a>

### Port.Direction


| Name | Number | Description |
| ---- | ------ | ----------- |
| INPUT | 0 |  |
| OUTPUT | 1 |  |
| INOUT | 2 |  |
| NONE | 3 |  |



<a name="vlsir-circuit-SpiceType"></a>

### SpiceType
Spice Type, used to identify what a component is in spice

| Name | Number | Description |
| ---- | ------ | ----------- |
| SUBCKT | 0 | The default value is implicitly SUBCKT |
| RESISTOR | 1 |  |
| CAPACITOR | 2 |  |
| INDUCTOR | 3 |  |
| MOS | 4 |  |
| DIODE | 5 |  |
| BIPOLAR | 6 |  |
| VSOURCE | 7 |  |
| ISOURCE | 8 |  |
| VCVS | 9 |  |
| VCCS | 10 |  |
| CCCS | 11 |  |
| CCVS | 12 |  |
| TLINE | 13 |  |


 

 

 



<a name="netlist-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## netlist.proto



<a name="vlsir-netlist-NetlistInput"></a>

### NetlistInput



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| pkg | [vlsir.circuit.Package](#vlsir-circuit-Package) |  | Circuit Package Content |
| netlist_path | [string](#string) |  | Destination Path |
| fmt | [NetlistFormat](#vlsir-netlist-NetlistFormat) |  | Netlist Format |
| result_path | [string](#string) |  | Result Path |






<a name="vlsir-netlist-NetlistResult"></a>

### NetlistResult



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| success | [bool](#bool) |  | True indicates success |
| fail | [string](#string) |  | Failure/ error message |





 


<a name="vlsir-netlist-NetlistFormat"></a>

### NetlistFormat


| Name | Number | Description |
| ---- | ------ | ----------- |
| UNSPECIFIED | 0 |  |
| SPECTRE | 1 |  |
| SPICE | 2 |  |
| NGSPICE | 3 |  |
| XYCE | 4 |  |
| HSPICE | 5 |  |
| CDL | 6 |  |
| VERILOG | 10 |  |


 

 


<a name="vlsir-netlist-Netlist"></a>

### Netlist
############################################################################
# `Netlist` Service
############################################################################

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| Netlist | [NetlistInput](#vlsir-netlist-NetlistInput) | [NetlistResult](#vlsir-netlist-NetlistResult) |  |

 



<a name="spice-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## spice.proto



<a name="vlsir-spice-AcInput"></a>

### AcInput
# AC Analysis Inputs


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| analysis_name | [string](#string) |  | (Optional) Analysis Name |
| fstart | [double](#double) |  | Start (min) frequency in Hz |
| fstop | [double](#double) |  | Stop (max) frequency in Hz |
| npts | [uint64](#uint64) |  | Number of points per interval of frequency sweep. |
| ctrls | [Control](#vlsir-spice-Control) | repeated | Control Elements |






<a name="vlsir-spice-AcResult"></a>

### AcResult
# AC Analysis Results 

AC analysis produces a set of complex-valued results, 
along with a single real-valued independent variable, which is always frequency.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| analysis_name | [string](#string) |  | (Optional) Analysis Name |
| freq | [double](#double) | repeated | Frequency Vector |
| signals | [string](#string) | repeated | Ordered signal names and quantities

FIXME: use `Signal` repeated Signal signals = 3; |
| data | [ComplexNum](#vlsir-spice-ComplexNum) | repeated | Primary Data Field. Of length `len(signals) * num_points`. |
| measurements | [AcResult.MeasurementsEntry](#vlsir-spice-AcResult-MeasurementsEntry) | repeated | Scalar measurement values |






<a name="vlsir-spice-AcResult-MeasurementsEntry"></a>

### AcResult.MeasurementsEntry



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [string](#string) |  |  |
| value | [double](#double) |  |  |






<a name="vlsir-spice-Analysis"></a>

### Analysis
# Analysis Union 

Enumerated analysis-input types. 
Primary component of a `Sim`.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| op | [OpInput](#vlsir-spice-OpInput) |  |  |
| dc | [DcInput](#vlsir-spice-DcInput) |  |  |
| tran | [TranInput](#vlsir-spice-TranInput) |  |  |
| ac | [AcInput](#vlsir-spice-AcInput) |  |  |
| noise | [NoiseInput](#vlsir-spice-NoiseInput) |  |  |
| sweep | [SweepInput](#vlsir-spice-SweepInput) |  |  |
| monte | [MonteInput](#vlsir-spice-MonteInput) |  |  |
| custom | [CustomAnalysisInput](#vlsir-spice-CustomAnalysisInput) |  |  |






<a name="vlsir-spice-AnalysisResult"></a>

### AnalysisResult
# Analysis Results Union 

Union of result-types for each `Analysis`.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| op | [OpResult](#vlsir-spice-OpResult) |  |  |
| dc | [DcResult](#vlsir-spice-DcResult) |  |  |
| tran | [TranResult](#vlsir-spice-TranResult) |  |  |
| ac | [AcResult](#vlsir-spice-AcResult) |  |  |
| noise | [NoiseResult](#vlsir-spice-NoiseResult) |  |  |
| sweep | [SweepResult](#vlsir-spice-SweepResult) |  |  |
| monte | [MonteResult](#vlsir-spice-MonteResult) |  |  |
| custom | [CustomAnalysisResult](#vlsir-spice-CustomAnalysisResult) |  |  |






<a name="vlsir-spice-ComplexNum"></a>

### ComplexNum
# Complex Number


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| re | [double](#double) |  |  |
| im | [double](#double) |  |  |






<a name="vlsir-spice-Control"></a>

### Control
# Control Elements Union


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| include | [Include](#vlsir-spice-Include) |  |  |
| lib | [LibInclude](#vlsir-spice-LibInclude) |  |  |
| save | [Save](#vlsir-spice-Save) |  |  |
| meas | [Meas](#vlsir-spice-Meas) |  |  |
| param | [vlsir.utils.Param](#vlsir-utils-Param) |  |  |
| literal | [string](#string) |  |  |






<a name="vlsir-spice-CustomAnalysisInput"></a>

### CustomAnalysisInput
# Custom Analysis Input

String-defined, non-first-class analysis statement. 
Primarily for simulator-specific specialty analyses.
Note the paired `Result` type is empty, 
as the schema has no means to comprehend externally-defined 
analysis data-shapes


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| analysis_name | [string](#string) |  | (Optional) Analysis Name |
| cmd | [string](#string) |  | String-literal analysis command |
| ctrls | [Control](#vlsir-spice-Control) | repeated | Control Elements |






<a name="vlsir-spice-CustomAnalysisResult"></a>

### CustomAnalysisResult
# Custom Analysis Result 

Does not return any data. Defined solely for filling slots in lists of analysis-results.






<a name="vlsir-spice-DcInput"></a>

### DcInput
# Dc Sweep Inputs


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| analysis_name | [string](#string) |  | (Optional) Analysis Name |
| indep_name | [string](#string) |  | Sweep Variable Name |
| sweep | [Sweep](#vlsir-spice-Sweep) |  | Sweep Data |
| ctrls | [Control](#vlsir-spice-Control) | repeated | Control Elements |






<a name="vlsir-spice-DcResult"></a>

### DcResult
# Dc Sweep Result 

Provides result data for a `Dc` analysis.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| analysis_name | [string](#string) |  | (Optional) Analysis Name |
| indep_name | [string](#string) |  | Independent Variable Name |
| signals | [string](#string) | repeated | Ordered signal names and quantities

FIXME: use `Signal` repeated Signal signals = 3; |
| data | [double](#double) | repeated | Primary Data Field |
| measurements | [DcResult.MeasurementsEntry](#vlsir-spice-DcResult-MeasurementsEntry) | repeated | Scalar measurement values |






<a name="vlsir-spice-DcResult-MeasurementsEntry"></a>

### DcResult.MeasurementsEntry



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [string](#string) |  |  |
| value | [double](#double) |  |  |






<a name="vlsir-spice-Include"></a>

### Include
# Include External Content


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| path | [string](#string) |  | File-system path FIXME: add more methods of specifying this |






<a name="vlsir-spice-LibInclude"></a>

### LibInclude
# Library &#34;Section&#34; Include

Commonly used for &#34;PVT corner&#34; inclusion, in which a single includable file 
often defines several named &#34;sections&#34;, e.g. &#34;TT&#34;, &#34;FF&#34;, &#34;SS&#34;, 
only one of which at a time may be included in a simulation.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| path | [string](#string) |  | File-system path FIXME: add more methods of specifying this |
| section | [string](#string) |  | Section name |






<a name="vlsir-spice-LinearSweep"></a>

### LinearSweep
# Linear Sweep


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| start | [double](#double) |  |  |
| stop | [double](#double) |  |  |
| step | [double](#double) |  |  |






<a name="vlsir-spice-LogSweep"></a>

### LogSweep
# Log Sweep


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| start | [double](#double) |  |  |
| stop | [double](#double) |  |  |
| npts | [double](#double) |  | FIXME: move to int |






<a name="vlsir-spice-Meas"></a>

### Meas
# Scalar Measurement


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| analysis_type | [string](#string) |  | Analysis Name (FIXME: or analysis-type) |
| name | [string](#string) |  | Measurement Name |
| expr | [string](#string) |  | Expression to be evaluated |






<a name="vlsir-spice-MonteInput"></a>

### MonteInput
# Monte Carlo Simulation Input

Define a set of child analyses to be simulated across `npts` randomly-generated circuit variations.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| analysis_name | [string](#string) |  | (Optional) Analysis Name |
| npts | [int64](#int64) |  | Number of points |
| seed | [int64](#int64) |  | Random-number seed |
| an | [Analysis](#vlsir-spice-Analysis) | repeated | Child Analyses |
| ctrls | [Control](#vlsir-spice-Control) | repeated | Control Elements |






<a name="vlsir-spice-MonteResult"></a>

### MonteResult
# Sweep Results


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| analysis_name | [string](#string) |  | (Optional) Analysis Name |
| variable | [string](#string) |  | Sweep-variable name |
| sweep | [Sweep](#vlsir-spice-Sweep) |  | Sweep-values |
| an | [AnalysisResult](#vlsir-spice-AnalysisResult) | repeated | Child Analysis Results FIXME: should these just be a flattened list, or organized by iteration |






<a name="vlsir-spice-NoiseInput"></a>

### NoiseInput
# Noise Analysis Inputs


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| analysis_name | [string](#string) |  | (Optional) Analysis Name |
| output_p | [string](#string) |  | Output Signal Name |
| output_n | [string](#string) |  | Output Signal Name, Negative. Optional, defaults to VSS. |
| input_source | [string](#string) |  | Input Source Name |
| fstart | [double](#double) |  | Start (min) frequency in Hz |
| fstop | [double](#double) |  | Stop (max) frequency in Hz |
| npts | [uint64](#uint64) |  | Number of points per interval of frequency sweep. |
| ctrls | [Control](#vlsir-spice-Control) | repeated | Control Elements |






<a name="vlsir-spice-NoiseResult"></a>

### NoiseResult
# Noise Analysis Results 

Noise analysis produces a set of complex-valued results, 
along with a single real-valued independent variable, which is always frequency.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| analysis_name | [string](#string) |  | (Optional) Analysis Name |
| signals | [string](#string) | repeated | Ordered signal names and quantities

FIXME: use `Signal` repeated Signal signals = 3; |
| data | [double](#double) | repeated | Primary Data Values Noise values are specified in per-Hz units, i.e. V^2/Hz for voltage noise, A^2/Hz for current noise. |
| integrated_noise | [NoiseResult.IntegratedNoiseEntry](#vlsir-spice-NoiseResult-IntegratedNoiseEntry) | repeated | Integrated noise values, mapped from signal name to value. |
| measurements | [NoiseResult.MeasurementsEntry](#vlsir-spice-NoiseResult-MeasurementsEntry) | repeated | Scalar measurement values |






<a name="vlsir-spice-NoiseResult-IntegratedNoiseEntry"></a>

### NoiseResult.IntegratedNoiseEntry



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [string](#string) |  |  |
| value | [double](#double) |  |  |






<a name="vlsir-spice-NoiseResult-MeasurementsEntry"></a>

### NoiseResult.MeasurementsEntry



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [string](#string) |  |  |
| value | [double](#double) |  |  |






<a name="vlsir-spice-OpInput"></a>

### OpInput
# Operating Point Inputs


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| analysis_name | [string](#string) |  | (Optional) Analysis Name |
| ctrls | [Control](#vlsir-spice-Control) | repeated | Control Elements |






<a name="vlsir-spice-OpResult"></a>

### OpResult
Operating Point Results


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| analysis_name | [string](#string) |  | (Optional) Analysis Name |
| signals | [string](#string) | repeated | Signal names and quantities

FIXME: use `Signal` repeated Signal signals = 3; |
| data | [double](#double) | repeated | Data values, in `signals` order |






<a name="vlsir-spice-PointSweep"></a>

### PointSweep
# Enumerated (List of Points) Sweep


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| points | [double](#double) | repeated |  |
| stop | [double](#double) |  |  |
| npts | [double](#double) |  |  |






<a name="vlsir-spice-Save"></a>

### Save
# Signal-Saving Controls


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| mode | [Save.SaveMode](#vlsir-spice-Save-SaveMode) |  |  |
| signal | [string](#string) |  |  |






<a name="vlsir-spice-Signal"></a>

### Signal
# Signal Declaration 

Declares a `Signal` name and type for output data.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| name | [string](#string) |  | Signal Name |
| quantity | [Signal.Quantity](#vlsir-spice-Signal-Quantity) |  |  |






<a name="vlsir-spice-SimInput"></a>

### SimInput
# Simulation Input 

Consists of: 
* The design under test (DUT) circuit `ckt`,
* Global simulator options, e.g. tolerance requirements, 
* A list of circuit-analyses to be completed, 
* An optional list of control-elements


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| pkg | [vlsir.circuit.Package](#vlsir-circuit-Package) |  | # Circuit Input The DUT circuit-package under test |
| top | [string](#string) |  | Top-level module (name) |
| opts | [SimOptions](#vlsir-spice-SimOptions) | repeated | # Simulation Configuration Input List of simulator options |
| an | [Analysis](#vlsir-spice-Analysis) | repeated | List of circuit analyses |
| ctrls | [Control](#vlsir-spice-Control) | repeated | Control elements. `SimInput` level controls are applied to *all* analyses. |






<a name="vlsir-spice-SimOptions"></a>

### SimOptions
# Simulator Options 
Global, cross-analysis settings.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| name | [string](#string) |  | Option name |
| value | [vlsir.utils.ParamValue](#vlsir-utils-ParamValue) |  | Option argument |






<a name="vlsir-spice-SimResult"></a>

### SimResult
# Simulation Result 
A list of results per analysis


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| an | [AnalysisResult](#vlsir-spice-AnalysisResult) | repeated |  |






<a name="vlsir-spice-Sweep"></a>

### Sweep
# Sweep Union


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| linear | [LinearSweep](#vlsir-spice-LinearSweep) |  |  |
| log | [LogSweep](#vlsir-spice-LogSweep) |  |  |
| points | [PointSweep](#vlsir-spice-PointSweep) |  |  |






<a name="vlsir-spice-SweepInput"></a>

### SweepInput
# Sweep 

The &#34;for loop&#34; of Spice analyses. 
Defines a scalar variable `var` to be swept, and a set of inner child-analyses
to be performed for each value of `var`. 
`Sweeps` themselves are `Analyses`, and therefore can be arbitrarily nested.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| analysis_name | [string](#string) |  | (Optional) Analysis Name |
| variable | [string](#string) |  | Sweep-variable name |
| sweep | [Sweep](#vlsir-spice-Sweep) |  | Sweep-values |
| an | [Analysis](#vlsir-spice-Analysis) | repeated | Child Analyses |
| ctrls | [Control](#vlsir-spice-Control) | repeated | Control Elements |






<a name="vlsir-spice-SweepResult"></a>

### SweepResult
# Sweep Results


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| analysis_name | [string](#string) |  | (Optional) Analysis Name |
| variable | [string](#string) |  | Sweep-variable name |
| sweep | [Sweep](#vlsir-spice-Sweep) |  | Sweep-values |
| an | [AnalysisResult](#vlsir-spice-AnalysisResult) | repeated | Child Analysis Results FIXME: should these just be a flattened list, or organized by sweep-value |






<a name="vlsir-spice-TranInput"></a>

### TranInput
# Transient Analysis Inputs


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| analysis_name | [string](#string) |  | (Optional) Analysis Name |
| tstop | [double](#double) |  | Stop Time |
| tstep | [double](#double) |  | Time-step requirement or recommendation |
| ic | [TranInput.IcEntry](#vlsir-spice-TranInput-IcEntry) | repeated | Initial Conditions. Mapping in the form of {signal-name: value} |
| ctrls | [Control](#vlsir-spice-Control) | repeated | Control Elements |






<a name="vlsir-spice-TranInput-IcEntry"></a>

### TranInput.IcEntry



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [string](#string) |  |  |
| value | [double](#double) |  |  |






<a name="vlsir-spice-TranResult"></a>

### TranResult
# Transient Analysis Results


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| analysis_name | [string](#string) |  | (Optional) Analysis Name |
| signals | [string](#string) | repeated | Ordered signal names and quantities

FIXME: use `Signal` repeated Signal signals = 3; |
| data | [double](#double) | repeated | Primary Data Field |
| measurements | [TranResult.MeasurementsEntry](#vlsir-spice-TranResult-MeasurementsEntry) | repeated | Scalar measurement values |






<a name="vlsir-spice-TranResult-MeasurementsEntry"></a>

### TranResult.MeasurementsEntry



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [string](#string) |  |  |
| value | [double](#double) |  |  |





 


<a name="vlsir-spice-Save-SaveMode"></a>

### Save.SaveMode
Enumerated Modes

| Name | Number | Description |
| ---- | ------ | ----------- |
| NONE | 0 |  |
| ALL | 1 |  |



<a name="vlsir-spice-Signal-Quantity"></a>

### Signal.Quantity
Physical Quantity

| Name | Number | Description |
| ---- | ------ | ----------- |
| VOLTAGE | 0 |  |
| CURRENT | 1 |  |
| NONE | 3 |  |


 

 


<a name="vlsir-spice-Spice"></a>

### Spice
# The SPICE Service

Defines a single method `Sim` which accepts simulator input via a `SimInput` message, 
performs the requested set of circuit-analyses, and returns results via a `SimResult`.

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| Sim | [SimInput](#vlsir-spice-SimInput) | [SimResult](#vlsir-spice-SimResult) |  |

 



<a name="tech-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## tech.proto



<a name="vlsir-tech-LayerInfo"></a>

### LayerInfo
Layers in PDKs roughly correspond to physical layers in the semiconductor
fabrication process. In this schema, a &#34;layer&#34; is a pair: first, some major
layer (like &#34;the first metal layer&#34;) and second, some sub-index into that
layer distinguishing the various purposes objects serve on the major layor.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| name | [string](#string) |  | A canonical shorthand name for the layer, e.g. &#34;met1&#34;. |
| purpose | [LayerPurpose](#vlsir-tech-LayerPurpose) |  |  |
| index | [uint64](#uint64) |  | An integer index identifying the major layer. |
| sub_index | [uint64](#uint64) |  | An integer index identifying the sub layer, or purpose. |






<a name="vlsir-tech-LayerPurpose"></a>

### LayerPurpose



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| description | [string](#string) |  | Short-hand description of the purpose of the sub-layer, e.g. &#34;drawing&#34;. |
| type | [LayerPurposeType](#vlsir-tech-LayerPurposeType) |  |  |






<a name="vlsir-tech-Package"></a>

### Package



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| name | [string](#string) |  | sky130_fd_sc_hd, sk130_fd_sc_hs, etc |






<a name="vlsir-tech-Technology"></a>

### Technology



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| name | [string](#string) |  | Skywater130, S130, Sky130, etc |
| packages | [Package](#vlsir-tech-Package) | repeated |  |
| layers | [LayerInfo](#vlsir-tech-LayerInfo) | repeated |  |





 


<a name="vlsir-tech-LayerPurposeType"></a>

### LayerPurposeType


| Name | Number | Description |
| ---- | ------ | ----------- |
| UNKNOWN | 0 |  |
| LABEL | 1 | Layers identified as LABEL will be used to attach net labels. |
| DRAWING | 2 |  |
| PIN | 3 |  |
| OBSTRUCTION | 4 |  |
| OUTLINE | 5 |  |


 

 

 



<a name="utils-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## utils.proto



<a name="vlsir-utils-AuthorMetadata"></a>

### AuthorMetadata
# Authorship Metadata

Summary information regarding authorship, ownership, and licensing
of any of several categories of design data.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| author | [string](#string) |  | Author Name |
| copyright | [string](#string) |  | Copyright Information |
| license | [string](#string) |  | License Information, in SPDX Format |






<a name="vlsir-utils-LibraryMetadata"></a>

### LibraryMetadata
# Library Metadata

Summary information about any of several categories of `Library`, including:
* Library domain
* (String) cell names
* Author information


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| domain | [string](#string) |  | Library Name / Domain |
| cell_names | [string](#string) | repeated | Cell Names |
| author | [AuthorMetadata](#vlsir-utils-AuthorMetadata) |  | Author Information |






<a name="vlsir-utils-Param"></a>

### Param
# Param Declaration
Named parameter with a sometimes over-ride-able value.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| name | [string](#string) |  | Param name |
| value | [ParamValue](#vlsir-utils-ParamValue) |  | Value, or default |
| desc | [string](#string) |  | Description |






<a name="vlsir-utils-ParamValue"></a>

### ParamValue
# Param-Value Enumeration

Supports the common param-types supported in legacy HDLs
such as Verilog and SPICE.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| bool_value | [bool](#bool) |  |  |
| int64_value | [int64](#int64) |  |  |
| double_value | [double](#double) |  |  |
| string_value | [string](#string) |  |  |
| literal | [string](#string) |  | Literal expressions, e.g. &#34;my_param1 * 5 &#43; sin(your_param3)&#34; |
| prefixed | [Prefixed](#vlsir-utils-Prefixed) |  | Metric-prefixed value, e.g. &#34;11n&#34;, &#34;15µ&#34; |






<a name="vlsir-utils-Prefixed"></a>

### Prefixed
# Prefixed
A quantity annotated with an `SIPrefix`


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| prefix | [SIPrefix](#vlsir-utils-SIPrefix) |  | The metric `SIPrefix` |
| int64_value | [int64](#int64) |  |  |
| double_value | [double](#double) |  |  |
| string_value | [string](#string) |  |  |






<a name="vlsir-utils-QualifiedName"></a>

### QualifiedName
# Domain-Qualified Name
Refers to an object outside its own namespace, at the global domain `domain`.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| domain | [string](#string) |  |  |
| name | [string](#string) |  |  |






<a name="vlsir-utils-Reference"></a>

### Reference
# Reference
Pointer to another Message, either defined in its own namespace (local) or
another (external).


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| local | [string](#string) |  | Local string-valued reference. Typically the `name` or similar field of the referent. |
| external | [QualifiedName](#vlsir-utils-QualifiedName) |  | Domain-qualified external reference |





 


<a name="vlsir-utils-SIPrefix"></a>

### SIPrefix
Enumerated SI Prefixes

| Name | Number | Description |
| ---- | ------ | ----------- |
| YOCTO | 0 | E-24 |
| ZEPTO | 1 | E-21 |
| ATTO | 2 | E-18 |
| FEMTO | 3 | E-15 |
| PICO | 4 | E-12 |
| NANO | 5 | E-9 |
| MICRO | 6 | E-6 |
| MILLI | 7 | E-3 |
| CENTI | 8 | E-2 |
| DECI | 9 | E-1 |
| DECA | 10 | E1 |
| HECTO | 11 | E2 |
| KILO | 12 | E3 |
| MEGA | 13 | E6 |
| GIGA | 14 | E9 |
| TERA | 15 | E12 |
| PETA | 16 | E15 |
| EXA | 17 | E18 |
| ZETTA | 18 | E21 |
| YOTTA | 19 | E24 |
| UNIT | 20 | Added v2.0

E0 |


 

 

 



## Scalar Value Types

| .proto Type | Notes | C++ | Java | Python | Go | C# | PHP | Ruby |
| ----------- | ----- | --- | ---- | ------ | -- | -- | --- | ---- |
| <a name="double" /> double |  | double | double | float | float64 | double | float | Float |
| <a name="float" /> float |  | float | float | float | float32 | float | float | Float |
| <a name="int32" /> int32 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint32 instead. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="int64" /> int64 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint64 instead. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="uint32" /> uint32 | Uses variable-length encoding. | uint32 | int | int/long | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a name="uint64" /> uint64 | Uses variable-length encoding. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum or Fixnum (as required) |
| <a name="sint32" /> sint32 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int32s. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="sint64" /> sint64 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int64s. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="fixed32" /> fixed32 | Always four bytes. More efficient than uint32 if values are often greater than 2^28. | uint32 | int | int | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a name="fixed64" /> fixed64 | Always eight bytes. More efficient than uint64 if values are often greater than 2^56. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum |
| <a name="sfixed32" /> sfixed32 | Always four bytes. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="sfixed64" /> sfixed64 | Always eight bytes. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="bool" /> bool |  | bool | boolean | boolean | bool | bool | boolean | TrueClass/FalseClass |
| <a name="string" /> string | A string must always contain UTF-8 encoded or 7-bit ASCII text. | string | String | str/unicode | string | string | string | String (UTF-8) |
| <a name="bytes" /> bytes | May contain any arbitrary sequence of bytes. | string | ByteString | str | []byte | ByteString | string | String (ASCII-8BIT) |

