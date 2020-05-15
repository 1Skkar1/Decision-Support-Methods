set N;   # set of cities
param lat{N};   # cities' latitude
param lng{N};   # cities' longitude
param pop{N};   # cities' population

# constants
param R := 6371.009;   # earth radius
param c{i in N} := ceil(pop[i] * 3 / 1000);
param pi := 3.14159265359;

# main variables: 
var dc_lat;   # distribution center's latitude
var dc_lng;   # distribution center's longitude

# auxiliary variables:
var dlat{N} >= 0;   # L1 distance component in latitude
var dlng{N} >= 0;   # L1 distance component in longitude
var d{N} >= 0;   # L1 distance (sum of lat + lng components)

minimize tdist: sum {i in N} c[i] * d[i];

subject to

latA {i in N}: dlat[i] >= 2 * pi * R * (dc_lat-lat[i])/360;
latB {i in N}: dlat[i] >= 2 * pi * R * (lat[i]-dc_lat)/360;
lngA {i in N}: dlng[i] >= 2 * pi * R * (dc_lng-lng[i])/360;
lngB {i in N}: dlng[i] >= 2 * pi * R * (lng[i]-dc_lng)/360;
dist {i in N}: d[i] = dlat[i] + dlng[i];

solve;

# display dlat, dlng, d;
printf "\n";
printf "*** minimizing total distance\n";
printf "Location of the DC: %g, %g \n",  dc_lat, dc_lng;
printf "Total distance: %.8g\n", tdist;
printf "Town closest to DC:   ";
printf {j in N: d[j] = min {i in N} d[i]} j;
printf "\n";
printf "Town with largest distributions costs:   ";
printf {j in N: c[j]*d[j] = max {i in N} c[i]*d[i]} j;
printf "\n";

end;