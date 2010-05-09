package com.googlecode.mustaine.testserver;

import org.mortbay.jetty.servlet.Context;
import org.mortbay.jetty.Server;

public class HTTPServer
{
  public static void main (String [] argv) throws Exception
  {
    Server server   = new Server(8080);  
    Context context = new Context(server, "/", Context.SESSIONS);
    
    context.addServlet(TestService.class, "/Test.service");
    // context.addServlet(ProtectedService.class, "/Protected.service");
    
    server.start();
  }
}
