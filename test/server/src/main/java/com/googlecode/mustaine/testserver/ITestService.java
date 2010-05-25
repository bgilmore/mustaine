package com.googlecode.mustaine.testserver;

import java.util.Date;

public interface ITestService
{  
  public void emptyCall();
  
  public Boolean returnBool(Boolean b);
  
  public Date returnDate(Date d);
  
  public double returnDouble(double d);
  
  public int returnInt(int i);
  
  public long returnLong(long l);
  
  public String returnString(String s);
  
  public String callThrowsException();

	public TemperatureOverview[] getShit();

	public TemperatureOverview objTest();
}
