#!/usr/bin/env python3
"""
Author: Matthew Downes
HW2
"""




def main():
	N = (160 * 1099511627776)/4096
	M = (512 * 1073741824)/4096 
	output = 1;
	i = 1;
	while (output >= .01):
		output = output * (((N-(i-1))-M) / (N-(i-1)))
		i = i + 1

	print(i)
	


if __name__ == '__main__':
  main()