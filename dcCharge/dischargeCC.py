setMode = lambda v, mode, channel:\
        v.write(f'FUNC {mode},(@{channel})')

setParam = lambda v, mode, value, channel:\
        v.write(f'{mode} {value},(@{channel})')


def setDischargeConst(v, mode, channel, curr, cfVolt, cfVoltParam, cfCap, cfCapParam):
    
    setCutoff = lambda v, condition, channel:\
        v.write(f'BATT:CUTO:{condition}:STAT ON, (@{channel})')

    setCutoffParam = lambda v, condition, value,channel: \
        v.write(f'BATT:CUTO:{condition} {value}, (@{channel})') 
    
    
    setMode(v,  mode, channel)
    setParam(v, mode, curr, channel)
    
    setCutoff(v, cfVolt, channel)
    setCutoffParam(v,cfVolt, cfVoltParam,channel)
    
    setCutoff(v, cfCap, channel)
    setCutoffParam(v,cfCap, cfCapParam, channel)

