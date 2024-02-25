import React, { useEffect } from 'react';
import * as msal from '@azure/msal-browser';

const msalConfig = {
  auth: {
    clientId: '1005217e-2daa-464c-8eb7-e6ff22e927f3',
    authority: 'https://login.microsoftonline.com/consumers',
    redirectUri: window.location.origin // Update with your redirect URI
  },
  cache: {
    cacheLocation: "localStorage", // This configures where your cache will be stored
    storeAuthStateInCookie: false, // Set this to "true" if you are having issues on IE11 or Edge
  },
};

const msalInstance = new msal.PublicClientApplication(msalConfig);

async function initializeMsal() {
  await msalInstance.initialize();
}

function Login(props) {

  // HANDLES REDIRECT OR CHECKS FOR EXISTING LOGIN TOKEN!
  useEffect(() => {
    initializeMsal().then(() => {
      if (props.user == null) {
        msalInstance.handleRedirectPromise().then((response) => {
          if (response && response.account) {
            props.setUser(response.account);
            console.log("Signed in as:\n", response.account);
          }
          else {
            const currentAccounts = msalInstance.getAllAccounts();
            if (currentAccounts.length > 0) {
              props.setUser(currentAccounts[0]);
              console.log("Signed in as:\n", currentAccounts[0]);
            }
            else {
              console.log("No accounts detected");
            }
          }
        });
      }
    });
  }, [props]);

  const handleLogin = async () => {
    const loginRequest = {
      scopes: ['user.read']
    };

    try {
      await msalInstance.loginRedirect(loginRequest);
      const account = msalInstance.getAccount();
      props.setUser(account);
      console.log("Signed in as:\n", account);
    } catch (error) {
      console.log(error);
    }
  };

  const handleLogout = () => {
    msalInstance.logoutRedirect();
    props.setUser(null);
  };

  return (
    <div>
      {props.user ? (
        <>
          <p>Hello {props.user.name}</p>
          <button onClick={handleLogout}>Logout</button>
        </>
      ) : (
        <>
          <p>
            Edit <code>src/App.js</code> and save to reload.
          </p>
          <button onClick={handleLogin}>Login with Microsoft</button>
        </>
      )}
    </div>
  );
}

export default Login;
