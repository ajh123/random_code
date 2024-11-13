local messageBoardAPI = {}

-- Base URL for the Flask API
local baseUrl

-- Function to set a new base URL
function messageBoardAPI.setBaseUrl(newUrl)
    baseUrl = newUrl
end

-- A helper function to perform HTTP requests with error checking and timeout using ComputerCraft's timer
local function performHttpRequest(url, method, body, headers, timeout)
    -- Start the HTTP request
    http.request {
        url = url,
        method = method,
        body = body,
        headers = headers
    }

    -- Start a timer for the timeout
    local timer = os.startTimer(timeout)

    while true do
        -- Wait for either a successful response, failure event, or timeout event
        local event, returnedUrl, p2, p3 = os.pullEvent()

        -- Handle success
        if event == "http_success" and returnedUrl == url then
            local response = p2.readAll()
            p2.close()
            os.cancelTimer(timer)  -- Cancel the timer since the request is complete
            return true, response
        end

        -- Handle failure with error details
        if event == "http_failure" and returnedUrl == url then
            local errorMsg = p2 -- Get the actual error message
            local errorCode = p3.getResponseCode()  -- Get the error code (status code)
            p3.close()
            os.cancelTimer(timer)  -- Cancel the timer since the request is complete
            return false, "Error " .. errorCode .. ": " .. errorMsg
        end

        -- Handle timeout
        if event == "timer" and returnedUrl == timer then
            os.cancelTimer(timer)  -- Cancel the timer to prevent further events
            return false, "Request timed out."
        end
    end
end

-- Wrapper for GET requests with a timeout (default 5 seconds)
local function httpGet(url, timeout)
    timeout = timeout or 5
    return performHttpRequest(url, "GET", nil, nil, timeout)
end

-- Wrapper for POST requests with a timeout (default 5 seconds)
local function httpPost(url, data, headers, timeout)
    timeout = timeout or 5
    return performHttpRequest(url, "POST", data, headers, timeout)
end

-- Wrapper for PUT requests with a timeout (default 5 seconds)
local function httpPut(url, data, headers, timeout)
    timeout = timeout or 5
    return performHttpRequest(url, "PUT", data, headers, timeout)
end

-- Wrapper for DELETE requests with a timeout (default 5 seconds)
local function httpDelete(url, headers, timeout)
    timeout = timeout or 5
    return performHttpRequest(url, "DELETE", nil, headers, timeout)
end

-- Function to get all message boards
function messageBoardAPI.getMessageBoards()
    return httpGet(baseUrl)
end

-- Function to get a specific message board by location
function messageBoardAPI.getMessageBoard(location)
    local ok, response = httpGet(baseUrl .. "/" .. location)
    if ok then
        local data = textutils.unserializeJSON(response)
        if data.error then
            return false, data.error
        else
            return true, data
        end
    else
        return false, "Failed to get message board."
    end
end

-- Function to create a new message board
function messageBoardAPI.createMessageBoard(location, x, z, num_lanes)
    local data = {
        location = location,
        x = x,
        z = z,
        num_lanes = num_lanes
    }
    local headers = {
        ["Content-Type"] = "application/json"
    }
    return httpPost(baseUrl, textutils.serializeJSON(data), headers)
end

-- Function to update an existing message board
function messageBoardAPI.updateMessageBoard(location, speed_limit, lane_statuses, message)
    local data = {
        speed_limit = speed_limit,
        lane_statuses = lane_statuses,
        message = message
    }
    local headers = {
        ["Content-Type"] = "application/json"
    }
    return httpPut(baseUrl .. "/" .. location, textutils.serializeJSON(data), headers)
end

-- Function to delete a message board
function messageBoardAPI.deleteMessageBoard(location)
    local headers = {
        ["Content-Type"] = "application/json"
    }
    return httpDelete(baseUrl .. "/" .. location, headers)
end

return messageBoardAPI
