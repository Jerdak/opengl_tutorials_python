 %module cimg
 %{
 /* Includes the header in the wrapper code */
 #include "CImg.h"
 %}
 
 /* Parse the header file to generate wrappers */
 %include "CImg.h"