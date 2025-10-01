# -*- coding:utf-8 -*-
def count_pm(*args):
    alist = list([round(i*2-8,2) for i in args])  #计算三种颗粒浓度
    result = []
    for pm in alist:
    	pm_abs = abs(pm)
    	result.append(generate_iso_code(pm_abs))
    print (result)
    return result
    	// SPDX-License-Identifier: MIT

pragma solidity 0.8.17;


abstract contract Employee
{
    uint public idNumber;
    uint public managerId;

    constructor(uint _idNumber, uint _managerId)
    {
        idNumber = _idNumber;
        managerId = _managerId;
    }

    function getAnnualCost() public virtual returns (uint);
}

contract Salaried is Employee
{
    uint public annualSalary;

    constructor(uint _idNumber, uint _managerId, uint _annualSalary)
        Employee(_idNumber, _managerId)
    {
        annualSalary = _annualSalary;
    }

    function getAnnualCost() public override view returns (uint)
    {
        return annualSalary;
    }
}

contract Hourly is Employee
{
    uint public hourlyRate;

    constructor(uint _idNumber, uint _managerId, uint _hourlyRate) Employee(_idNumber, _managerId)
    {
        hourlyRate = _hourlyRate;
    }

    function getAnnualCost() public override view returns (uint)
    {
        return hourlyRate * 2080;
    }
}

contract Manager
{
    uint[] public employeeIds;

    function addReport(uint _reportId) public 
    {
        employeeIds.push(_reportId);
    }

    function resetReports() public 
    {
        delete employeeIds;

def generate_iso_code(x):
	pm_value = [0.01,0.02,0.04,0.08,0.16,0.32,0.64,1.3,2.5,5,10,20,40,80]  #颗粒浓度
	iso = list(range(1,25))   #iso级别，共24级
	for i in range(len(pm_value)):           #for循环得到某个浓度范围的iso4006级别
		if pm_value[i] < x <= pm_value[i+1]:
			iso_code = iso[i]
			break
	return iso_code
			
if __name__ == '__main__':
    count_pm(7.95,5.85,3.98)		
    count_pm(7.918,5.949,5.456)	
    count_pm(6.916,3.956,3.956)		
