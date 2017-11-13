

An application owner is deploying their new application and set of application services. The application consists of the web front end:  www.myapp.com where the CSS is stored.  Then there is the set of app services to that hold the images https://myapp.com/images, then there is the videos:  https://myapp.com/videos and then the app services that deal with advertising process out to the 3rd party ad servers https://myapp.com/ads (which then goes to https:/thirdparty.com/ad_server/location/co/den/)

So when the application owner wants to deploy their application, they want to have corresponding pools and place these rules to direct to those pools
PoolA:https://www.myapp.com
PoolB: https://myapp.com/images
PoolC: https://myapp.com/videos