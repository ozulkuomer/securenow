import React, {useState} from "react";
import { User, UserFactory } from "../../models/user";
import { ApiResponse } from "../../models/api_response";


async function handle_status_send(email?:string, password?:string):Promise<User | null>{

	if(!email || !password){
		return null;
	}

	const response = await fetch(`http://localhost:5000/api/auth/login`, {
		method:'POST',
		headers:{
			'Content-Type' : 'application/json',
		},
		body:JSON.stringify({email, password})
	})
	if(response.status >= 400){
		return null;
	}
	const body = await response.json() as ApiResponse<User>
	if(body.payload){
		return body.payload[0]
	}
	return null;
}

export function LoginPage(props:{set_user:(user:User) => void}) {

	const [email, set_email] = useState<string>('');
	const [password, set_password] = useState<string>('');
	const {set_user} = props;

	return (
		<div className={'login-container'}>
			<h1>Social Book</h1>
			<form>
				<div className={'row'}>
					<label htmlFor="email">Enter your email:</label>
					<input type="email" id="email" name="email" value={email} onChange={(event) => set_email(event.target.value)} />
				</div>
				<div className={'row'}>
					<label htmlFor="pwd">Password:</label>
					<input type="password" id="pwd" name="pwd" value={password} onChange={(event) => set_password(event.target.value)}  />

				</div>
				<div className={'row'}>
					<button type="button" disabled={email?.length === 0 || password?.length === 0} onClick={async () => {
						try{
							const response = await handle_status_send(email, password);
							if(response){
								set_user(UserFactory.create_instance(response))
							}
						}catch (err){
							console.log('login err');
						}
					}} >
						Giriş Yap
					</button>

				</div>

			</form>
		</div>
	)
}
