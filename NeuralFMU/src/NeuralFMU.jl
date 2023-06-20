##
module NeuralFMU

using FMI
using FMIFlux
using Flux

function main()
    fmu = fmiLoad("../orbit_dynamics.fmu")

    tstart = 0.0
    tstep = 0.001
    tstop = 1000.0

    param = Dict("m" => 4.0)
    vars = ["x_out[1]", "x_out[2]", "x_out[3]", "v_out[1]", "v_out[2]", "v_out[3]"]

    input = [0.3, 0.5, -0.2]

    fmudata = fmiSimulate(fmu, (tstart, tstop); parameters=param, inputValueReferences=fmu.modelDescription.inputValueReferences, inputFunction=x -> input, recordValues=vars, saveat=tstart:tstep:tstop)

    numInputs = length(fmu.modelDescription.inputValueReferences)
    numOutputs = length(fmu.modelDescription.outputValueReferences)

    net = Chain(u -> fmu(;u_refs=fmu.modelDescription.inputValueReferences, u=u, y_refs=fmu.modelDescription.outputValueReferences),
                Dense(numOutputs, 16, tanh),
                Dense(16, 16, tanh),
                Dense(16, numOutputs))
    end

end # module NeuralFMU
##