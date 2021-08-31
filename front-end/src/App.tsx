import React, {useState}        from 'react';
import { HomePage } from "./pages/home/home";
import { SWRConfig } from 'swr'
import { User } from "./models/user";
import { LoginPage } from "./pages/login/login";


function App() {
    const [user, set_user] = useState<User>();

    return (
    <div className="App">
        <SWRConfig
            value={{
                refreshInterval: 3000,
                fetcher: (resource, init) => fetch(resource, init).then(res => {
                    if (res.status === 401) {
                        if (window) {
                            window.location.href = `/login?ref=${res.url}`;
                        }
                        return Promise.reject();
                    }
                    return res.json();
                })
            }}
        >
            {
                user ? <HomePage  /> : <LoginPage set_user={(user:User) => {set_user(user)}} />
            }
        </SWRConfig>
    </div>
  );
}

export default App;
