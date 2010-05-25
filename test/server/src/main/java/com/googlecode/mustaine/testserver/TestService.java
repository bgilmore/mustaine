package com.googlecode.mustaine.testserver;

import com.caucho.hessian.server.HessianServlet;
import java.util.Date;

import com.googlecode.mustaine.testserver.TemperatureOverview;

public class TestService extends HessianServlet implements ITestService
{
  public void emptyCall() {
    ;
  }
  
  public Boolean returnBool(Boolean b) {
    return b;
  }
  
  public Date returnDate(Date d) {
    return d;
  }
  
  public double returnDouble(double d) {
    return d;
  }
  
  public int returnInt(int i) {
    return i;
  }
  
  public long returnLong(long l) {
    return l;
  }
  
  public String returnString(String s) {
    return s;
  }
  
  public String callThrowsException() {
      throw new IllegalArgumentException("Your argument is illegal!");
  }

	public TemperatureOverview[] getShit() {
			TemperatureOverview[] shit = new TemperatureOverview[2];
			TemperatureOverview obj = new TemperatureOverview();
			
			obj.setGreenAssetCount(3);
			obj.setYellowAssetCount(2);
			obj.setRedAssetCount(1);
			
			shit[0] = shit;
			shit[1] = obj;
			
			
			return shit;
	}

	public TemperatureOverview objTest() {
			TemperatureOverview obj = new TemperatureOverview();
			
			obj.setGreenAssetCount(3);
			obj.setYellowAssetCount(2);
			obj.setRedAssetCount(1);
			
			return obj;
	}
}
