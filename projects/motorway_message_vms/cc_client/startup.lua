local messageBoardAPI = require "board_api"

local monitors = {
    ["general"] = peripheral.wrap("monitor_0"),
    ["1"] = peripheral.wrap("monitor_1"),
    ["2"] = peripheral.wrap("monitor_2"),
    ["3"] = peripheral.wrap("monitor_3")
}

local baseUrl = "http://10.0.0.78:5000/message_boards"
messageBoardAPI.setBaseUrl(baseUrl)

local name = os.getComputerLabel()
local x, _, z = gps.locate()

if x == nil then
    error("Cannot get GPS position.")
end

local lanes = 3


messageBoardAPI.createMessageBoard(name, x, z, lanes)

-- Function to print centered text on a specific line of a specified monitor
local function printCentered(monitor, text, y)
    local width, _ = monitor.getSize() -- Get monitor width
    local x = math.floor((width - #text) / 2) + 1 -- Calculate centered x position
    monitor.setCursorPos(x, y) -- Set the cursor to the calculated position
    monitor.write(text) -- Write the text
end


local function monitorPrint(monitor, text)
    if monitor then
        monitor.clear()
        monitor.setCursorPos(1, 1)

        -- Get monitor width to handle text wrapping
        local width, _ = monitor.getSize()
        
        local line = ""
        for word in text:gmatch("%S+") do
            if #line + #word + 1 > width then
                monitor.write(line)
                monitor.setCursorPos(1, select(2, monitor.getCursorPos()) + 1)
                line = word
            else
                line = line .. (line == "" and "" or " ") .. word
            end
        end
        monitor.write(line)  -- Write the last line
    else
        print("Monitor not found!")
    end
end

while true do
    sleep(3)
    local ok, response = messageBoardAPI.getMessageBoard(name)

    if ok then
        monitors["general"].setCursorPos(1, 1)
        monitors["general"].clear()
        monitors["general"].setTextScale(5)
        monitorPrint(monitors["general"], response.general_message)
        print("====")
        print("Message: "..response.general_message)
        print("Spped limit:"..response.speed_limit)
        print("Lanes:")
        for index, value in pairs(response.lane_statuses) do
            print(index, value)
            monitors[index].setCursorPos(1, 1)
            monitors[index].clear()
            monitors[index].setTextScale(5)
            if value == true then
                monitors[index].setTextColor(colors.white)
                if response.general_message == "End" then
                    printCentered(monitors[index], "End", 1)
                else
                    if response.speed_limit >= 0 then
                        printCentered(monitors[index], tostring(response.speed_limit), 1)
                    end
                end
            else
                monitors[index].setTextColor(colors.red)
                printCentered(monitors[index], "X", 1)
            end
        end
    end
end

messageBoardAPI.deleteMessageBoard(name)