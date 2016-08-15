# F5 Stats Emitter API Reference 
## Overview

Provides the back-end library for sending events and stats to a data-collection
service (e.g. LEO, Splunk).

## Node module usage
```javascript
let statsEmitter = require('stats-emitter')
```

## Transport Class
Before stats can be sent to an external service, a transport type must be specified to 
indicate the method that will be used to transmit the stats.  The transport type will
be specified when creating a collector object (discussed below).

Currently, there are two options that are supported:
  
```javascript
// use an HTTP POST request to send stats to a listening service
statsEmitter.networkTransport;
// return the stats to a caller-supplied callback for printing to a file or console
statsEmitter.internalTransport;
```

## Collector Class
The collector class is used to create the required format for the collector that
will be receiving the stats.  Currently two formats are supported:  LEO and Splunk.

The caller must create an object of the desired class using the following:

### LEO Collector
```javascript
let collector = new statsEmitter.LeoCollector( {
   collectorHost: leoHost,
   collectorPort: leoPort,
   protocol: leoProtocol,
   host: appHost,
   source: source,
   sourceType: sourceType,
   facility: facility,
   deviceGroup: deviceGroup,
   tenant: tenant,
   authToken: token,
}, transportType );
```

### Splunk Collector
```javascript
let collector = new statsEmitter.SplunkCollector( {
   collectorHost: splunkHost,
   collectorPort: splunkPort,
   protocol: splunkProtocol,
   host: appHost,
   source: source,
   sourceType: sourceType,
   authToken: token,
}, transportType );
```

## Sending Stats and Events
Once a collector object has been created, stats can be sent as
key-value pairs a JSON property object and the following syntax:
```javascript
collector.sendStats(stats1, sendStasCb)
collector.sendStats(stats2, sendStasCb)
```
Once this call is made, the caller should not use the stats object
except to delete it.

## Test App
The testapp has options for sending data to Splunk (or an http service) or the console.
It will send a series of stats and then exit. 

The syntax of the test app is:
```script
$ nodejs lib/stats-emitter/test/example.js [ leo | splunk [ redirect [ console | file filename ] ] ]
```
The test app assumes a splunk/leo server is running on the local host and listening on
port 8080. To change this, you must edit example.js.
```
