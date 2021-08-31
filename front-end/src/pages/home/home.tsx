import { Layout } from "../../layout/layout";
import "./home.css";
import {useState, useEffect} from "react";
import { Status, StatusFactory } from "../../models/status";
import useSWR from 'swr';
import { ApiResponse } from "../../models/api_response";


const API_URL = 'http://localhost:5000/api';

async function handle_status_send(status:Partial<Status>){
	if(!status){
		throw new Error('Status text not found');
	}
	return await fetch(`${API_URL}/status`, {
		method:'POST',
		headers:{
			'Content-Type' : 'application/json',
		},
		body:JSON.stringify(StatusFactory.create_instance(status))
	})

}

export function HomePage()
{
	const [new_status_text, set_new_status_text] = useState<string>('');
	const [status_list, set_status_list] = useState<Status[]>([]);
	const {data:status_list_response, mutate:statues_mutate} = useSWR<ApiResponse<Status>>(`${API_URL}/status`);

	useEffect(() => {
		if(status_list_response){
			set_status_list(status_list_response?.payload || []);
		}
	}, [status_list_response]);



	return (<Layout>
		<div className="card status">
			<span>Ne düşünüyorsun?</span>
			<textarea value={new_status_text} onChange={(event) => set_new_status_text(event.target.value)} name="" id="" cols={30} rows={10}>

			</textarea>
			<button onClick={() =>handle_status_send({text:new_status_text, user_id : 1})
				.then(() => {
					statues_mutate();
					set_new_status_text('');
				})
				.catch((err) => console.log('err', err))} disabled={new_status_text.length === 0} className="button">Send</button>
		</div>

		<div className="time_line_flow">
			{
				status_list.map((status, index) => (<div key={`status_${index}`} className="card">
					{status.text}
				</div>))
			}

		</div>

	</Layout>)
}
