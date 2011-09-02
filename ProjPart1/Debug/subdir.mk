################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../find_obj.cpp \
../generic_descriptor_match.cpp \
../panograph.cpp 

OBJS += \
./find_obj.o \
./generic_descriptor_match.o \
./panograph.o 

CPP_DEPS += \
./find_obj.d \
./generic_descriptor_match.d \
./panograph.d 


# Each subdirectory must supply rules for building sources it contributes
%.o: ../%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: Cross G++ Compiler'
	g++ -g -I/usr/local/include -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


