set N;   # set of cities
param lat{N};   # cities' latitude
param lng{N};   # cities' longitude
param pop{N};   # cities' population

# constants
param R := 6371.009;   # earth radius
param pi := 3.14159265359;
param c {i in N, j in N} := ceil(pop[i] * 3 / 1000) *
      2 * pi * R * (abs(lat[i]-lat[j]) + abs(lng[i]-lng[j]))/360;
param f {j in N} := 25000;
param maxDCs;

# main variables: 
var x{i in N, j in N} binary;   # 1 if city i is served by DC j
var y{j in N} binary;   # selected distribution centers

minimize tcost: sum {i in N, j in N} c[i,j] * x[i,j] + sum {j in N} f[j] * y[j];

subject to

open {i in N, j in N}: x[i,j] <= y[j];
serve {i in N}: sum {j in N} x[i,j] = 1;
maxopen: sum {j in N} y[j] <= maxDCs;

printf("*** Minimizing total cost ***\n");
solve;

printf "Distribution costs per town (fixed, delivery)\n";
printf {j in N} "%30s\t%g\t%g\n", j, f[j]*y[j], sum {k in N} c[j,k] * x[j,k];
printf "\nTotal cost: %16.10g\n", tcost;
printf("\nOpen DCs:\n");
printf {j in N: y[j] > 0.5} "\t%s\n", j;
printf "\nTown with largest delivery costs:   ";
printf {i in N: sum {j in N} c[i,j]*x[i,j] = max {k in N} sum {j in N} c[k,j]*x[k,j]} i;
printf "\n";
end;