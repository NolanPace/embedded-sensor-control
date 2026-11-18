"""Serial-compatible CSV telemetry parser, statistics and a hardware-free simulator."""
from __future__ import annotations
from dataclasses import dataclass
from math import sin,pi
import argparse,csv,random,statistics

@dataclass(frozen=True)
class Reading:
    timestamp_ms:int
    voltage:float
    filtered_voltage:float
    control_output:float

def parse(line:str)->Reading:
    fields=line.strip().split(',')
    if len(fields)!=4:raise ValueError('Expected four CSV values')
    try:r=Reading(int(fields[0]),*[float(f) for f in fields[1:]])
    except ValueError as err:raise ValueError('Invalid telemetry number') from err
    if r.timestamp_ms<0 or not (0<=r.voltage<=3.3 and 0<=r.filtered_voltage<=3.3 and 0<=r.control_output<=1):
        raise ValueError('Telemetry out of expected range')
    return r

def simulate(count:int=100,seed:int=42):
    if count<0:raise ValueError('Count must be nonnegative')
    rng=random.Random(seed);filtered=0.0
    for i in range(count):
        v=min(3.3,max(0,1.65+0.9*sin(i/12)+rng.gauss(0,.07)))
        filtered=.15*v+.85*filtered
        control=max(0,min(1,.5+.25*(1.65-filtered)))
        yield Reading(i*100,round(v,4),round(filtered,4),round(control,4))

def summary(readings:list[Reading])->dict:
    if not readings:return {'samples':0,'mean_voltage':None,'max_voltage':None,'mean_control_output':None}
    return {'samples':len(readings),'mean_voltage':round(statistics.mean(r.voltage for r in readings),3),'max_voltage':max(r.voltage for r in readings),'mean_control_output':round(statistics.mean(r.control_output for r in readings),3)}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--simulate',action='store_true')
    parser.add_argument('--count',type=int,default=100)
    parser.add_argument('--output',default='telemetry.csv')
    parser.add_argument('--input',help='Read existing MCU CSV file')
    args=parser.parse_args()
    if args.simulate:
        readings=list(simulate(args.count));
        with open(args.output,'w',newline='') as file:
            writer=csv.writer(file);writer.writerow(Reading.__dataclass_fields__.keys())
            writer.writerows(tuple(vars(r).values()) for r in readings)
        print('Wrote',args.output,summary(readings))
    elif args.input:
        with open(args.input,newline='') as file:
            next(file,None)
            readings=[parse(line) for line in file if line.strip()]
        print(summary(readings))
    else:parser.print_help()
if __name__=='__main__':main()
