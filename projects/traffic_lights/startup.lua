-- Traffic Light Configuration
-- Version = Traffic Light Shape
-- Enter 1 for block
-- Enter 2 for arrow left
-- Enter 3 for arrow forward
-- Enter 4 for arrow right
-- Enter 5 for round
-- Phase = a unique number to group lights together.
local trafficLights = {
    {monitor = peripheral.wrap("monitor_25"), phase = 1, shape = 1},
    {monitor = peripheral.wrap("monitor_24"), phase = 2, shape = 1},
    {monitor = peripheral.wrap("monitor_21"), phase = 3, shape = 1},
}

-- Traffic Light Sequence Mode
-- Enter 1 for standard
-- Enter 2 for British/German
-- Enter 3 for warning
-- Enter 4 for stop light
local sequence = 1

-- Yellow or Orange? Depending on your country, the color may differ
-- Enter 1 for orange
-- Enter 2 for yellow
local middle = 1

-- Time Customisation
local timeforgreen = 10     -- time for green light per phase
local timeforyellow = 3     -- time for yellow light per phase
local timeforturnred = 1    -- pause after red light
local warninginterval = 1   -- warning light flash interval

-- ******************************
-- CODE BELOW IS NOT ADJUSTABLE!!
-- ******************************

local function openAllModems()
    local peripherals = peripheral.getNames()

    for _, name in ipairs(peripherals) do
        if peripheral.getType(name) == "modem" then
            rednet.open(name)
        end
    end
end

openAllModems()

local middleColor = middle == 1 and colors.orange or colors.yellow

-- Helper function to reset a monitor
local function reset(mon)
    mon.setBackgroundColor(colors.black)
    mon.clear()
end

-- Traffic Light Setting Functions

function redLight(monId)
    mon = trafficLights[monId].monitor

	mon.setBackgroundColor(colors.red)
	lightShape = trafficLights[monId].shape

	if lightShape == 1 then shapeBlock(mon, "red")
	elseif lightShape == 2 then shapeLeftArrow(mon, "red")	
	elseif lightShape == 3 then shapeForwardArrow(mon, "red")
	elseif lightShape == 4 then shapeRightArrow(mon, "red")
	elseif lightShape == 5 then shapeRound(mon, "red")
	end
end

function yellowLight(monId)
    mon = trafficLights[monId].monitor

	mon.setBackgroundColor(middleColor)
	lightShape = trafficLights[monId].shape

	if lightShape == 1 then	shapeBlock(mon, "yellow")
	elseif lightShape == 2 then shapeLeftArrow(mon, "yellow")
	elseif lightShape == 3 then shapeForwardArrow(mon, "yellow")
	elseif lightShape == 4 then shapeRightArrow(mon, "yellow")
	elseif lightShape == 5 then shapeRound(mon, "yellow")
	end
end

function greenLight(monId)
    mon = trafficLights[monId].monitor

	mon.setBackgroundColor(colors.green)
	lightShape = trafficLights[monId].shape

	if lightShape == 1 then shapeBlock(mon, "green")
	elseif lightShape == 2 then shapeLeftArrow(mon, "green")
	elseif lightShape == 3 then	shapeForwardArrow(mon, "green")
	elseif lightShape == 4 then shapeRightArrow(mon, "green")
	elseif lightShape == 5 then shapeRound(mon, "green")		
	end
end

-- Draw Shape Functions

function shapeBlock(mon, lightSelected)
	if lightSelected == "red" then
		line1, line2, line3, line4, line5, line6 = 2,3,4,5,6,7
	elseif lightSelected == "yellow" then
		line1, line2, line3, line4, line5, line6 = 10,11,12,13,14,15
	elseif lightSelected == "green" then
		line1, line2, line3, line4, line5, line6 = 18,19,20,21,22,23
	end

	mon.setCursorPos(4,line1)
	mon.write("         ")
	mon.setCursorPos(4,line2)
	mon.write("         ")
	mon.setCursorPos(4,line3)
	mon.write("         ")
	mon.setCursorPos(4,line4)
	mon.write("         ")
	mon.setCursorPos(4,line5)
	mon.write("         ")
	mon.setCursorPos(4,line6)
	mon.write("         ")
end

function shapeLeftArrow(mon, lightSelected)
	if lightSelected == "red" then
		line1, line2, line3, line4, line5, line6, line7, line8 = 1,2,3,4,5,6,7,8
	elseif lightSelected == "yellow" then
		line1, line2, line3, line4, line5, line6, line7, line8 = 9,10,11,12,13,14,15,16
	elseif lightSelected == "green" then
		line1, line2, line3, line4, line5, line6, line7, line8 = 17,18,19,20,21,22,23,24
	end

	mon.setCursorPos(5,line1)
	mon.write("  ")
	mon.setCursorPos(4,line2)
	mon.write("   ")
	mon.setCursorPos(3,line3)
	mon.write("    ")
	mon.setCursorPos(2,line4)
	mon.write("             ")
	mon.setCursorPos(2,line5)
	mon.write("             ")
	mon.setCursorPos(3,line6)
	mon.write("    ")
	mon.setCursorPos(4,line7)
	mon.write("   ")
	mon.setCursorPos(5,line8)
	mon.write("  ")
end

function shapeForwardArrow(mon, lightSelected)
	if lightSelected == "red" then
		line1, line2, line3, line4, line5, line6, line7, line8, line9 = 1,2,3,4,5,6,7,8,9
	elseif lightSelected == "yellow" then
		line1, line2, line3, line4, line5, line6, line7, line8, line9 = 9,10,11,12,13,14,15,16,17
	elseif lightSelected == "green" then
		line1, line2, line3, line4, line5, line6, line7, line8, line9 = 16,17,18,19,20,21,22,23,24
	end

	mon.setCursorPos(7,line1)
	mon.write("  ")
	mon.setCursorPos(6,line2)
	mon.write("    ")
	mon.setCursorPos(5,line3)
	mon.write("      ")
	mon.setCursorPos(4,line4)
	mon.write("        ")
	mon.setCursorPos(4,line5)
	mon.write("        ")
	mon.setCursorPos(7,line6)
	mon.write("  ")
	mon.setCursorPos(7,line7)
	mon.write("  ")
	mon.setCursorPos(7,line8)
	mon.write("  ")
	mon.setCursorPos(7,line9)
	mon.write("  ")
end

function shapeRightArrow(mon, lightSelected)
	if lightSelected == "red" then
		line1, line2, line3, line4, line5, line6, line7, line8 = 1,2,3,4,5,6,7,8
	elseif lightSelected == "yellow" then
		line1, line2, line3, line4, line5, line6, line7, line8 = 9,10,11,12,13,14,15,16
	elseif lightSelected == "green" then
		line1, line2, line3, line4, line5, line6, line7, line8 = 17,18,19,20,21,22,23,24
	end

	mon.setCursorPos(10,line1)
	mon.write("  ")
	mon.setCursorPos(10,line2)
	mon.write("   ")
	mon.setCursorPos(10,line3)
	mon.write("    ")
	mon.setCursorPos(2,line4)
	mon.write("             ")
	mon.setCursorPos(2,line5)
	mon.write("             ")
	mon.setCursorPos(10,line6)
	mon.write("    ")
	mon.setCursorPos(10,line7)
	mon.write("   ")
	mon.setCursorPos(10,line8)
	mon.write("  ")
end

function shapeRound(mon, lightSelected)
	if lightSelected == "red" then
		line1, line2, line3, line4, line5, line6, line7, line8 = 1,2,3,4,5,6,7,8
	elseif lightSelected == "yellow" then
		line1, line2, line3, line4, line5, line6, line7, line8 = 9,10,11,12,13,14,15,16
	elseif lightSelected == "green" then
		line1, line2, line3, line4, line5, line6, line7, line8 = 17,18,19,20,21,22,23,24
	end

	mon.setCursorPos(5,line1)
	mon.write("       ")
	mon.setCursorPos(4,line2)
	mon.write("         ")
	mon.setCursorPos(3,line3)
	mon.write("           ")
	mon.setCursorPos(2,line4)
	mon.write("             ")
	mon.setCursorPos(2,line5)
	mon.write("             ")
	mon.setCursorPos(3,line6)
	mon.write("           ")
	mon.setCursorPos(4,line7)
	mon.write("         ")
	mon.setCursorPos(5,line8)
	mon.write("       ")
end

-- Sequence functions
local function processPhase(currentPhase, nextPhase)
    -- Set current phase green and others red
    for id, light in ipairs(trafficLights) do
        reset(light.monitor)
        if light.phase == currentPhase then
            greenLight(id)
        else
            redLight(id)
        end
    end
    sleep(timeforgreen)

    -- Set current phase yellow
    for id, light in ipairs(trafficLights) do
        if light.phase == currentPhase then
            reset(light.monitor)
            yellowLight(id)
        end
    end
    sleep(timeforyellow)

    -- Transition to the next phase
    for id, light in ipairs(trafficLights) do
        reset(light.monitor)
        redLight(id)
    end
    sleep(timeforturnred)
end

local function standardSequence()
    local phases = {}
    for _, light in ipairs(trafficLights) do
        phases[light.phase] = true
    end
    local phaseOrder = {}
    for phase in pairs(phases) do
        table.insert(phaseOrder, phase)
    end
    table.sort(phaseOrder) -- Ensure phases are processed in order

    while true do
        for i = 1, #phaseOrder do
            local currentPhase = phaseOrder[i]
            local nextPhase = phaseOrder[i % #phaseOrder + 1]
            processPhase(currentPhase, nextPhase)
        end
    end
end

local function warningSequence()
    while true do
        for _, light in ipairs(trafficLights) do
            reset(light.monitor)
            setYellowLight(light.monitor)
        end
        sleep(warninginterval)
        for _, light in ipairs(trafficLights) do
            reset(light.monitor)
        end
        sleep(warninginterval)
    end
end

local function stopSequence()
    while true do
        for _, light in ipairs(trafficLights) do
            reset(light.monitor)
            setRedLight(light.monitor)
        end
        sleep(warninginterval)
    end
end

-- Entry point
local function start()
    if sequence == 1 then
        standardSequence()
    elseif sequence == 3 then
        warningSequence()
    elseif sequence == 4 then
        stopSequence()
    else
        print("Unsupported sequence type!")
    end
end

start()
