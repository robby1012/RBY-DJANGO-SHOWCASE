module.exports = function($http, $window, Upload)
{
    let requestHTTP = function(target, data, request_type="text")
    {
        // ____this function is serve as http request for the each categories upload, sendGet
        // and even just send. each request has different type of parameters____
        let param_ = {
            "url": target,
            "method": data.method,
            "headers": {}
        }
        
        // ____if use authentication token____
        if(typeof data.authentication !== "undefined")
            param_.headers["Authorization"] = "Token " + data.authentication;

        // ____if using the data parameter____
        if(typeof data.data !== "undefined")
            param_.data = data.data;

        // ____if any headers____
        if(typeof data.headers !== "undefined")
            if (typeof param_.headers !== "undefined"){
                param_.headers = Object.assign(param_.headers, data.headers);
            } else {
                param_.headers = data.headers;
            }
            
        if (request_type == "upload")
            return Upload.upload(param_);

        return $http(param_);
    }

    return {
        // ** UPLOAD HTTP REQUEST **
        "sendAsFormData": function(method, target, data)
        {
            // ____this will serve the request upload http. the parameter required
            // method(post, patch, put, or delete), target is endpoint target, and data is
            // data body that need to be sent____
            data["method"] = method;

            // ____return the requestHTTP function with parameters____
            return requestHTTP(target, data, "upload");
        },
        // ** COMMON SEND HTTP REQUEST **
        "sendAsJson": function(method, target, data)
        {
            // ____this will serve same as above function but it only serve the common data.
            // the parameter required method(post, patch, put, or delete), target is endpoint target,
            // and data is data body that need to be sent____
            data["method"] = method;
            data["headers"] = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            // ____return the requestHTTP function with parameters____
            return requestHTTP(target, data, "text");
        },
        // ** ONLY GET HTTP REQUEST **
        "sendGet": function(target, authentication=null)
        {
            // ____this serve different that previous function, it only serve the GET method
            // parameter request http, just only need the target and authentication if required____
            let data = {method: "get"};

            if (authentication != null)
                data["authentication"] = authentication;

            // ____return the requestHTTP function with parameters____
            return requestHTTP(target, data, "text");
        }
    }
}