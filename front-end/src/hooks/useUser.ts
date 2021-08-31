import useSWR from "swr";
import { ApiResponse } from "../models/api_response";
import { User } from "../models/user";
import { KeyedMutator } from "swr/dist/types";

const API_URL = 'http://localhost:5000/api';


export function useUser ():{user:User | undefined, isLoading:boolean, user_mutate:KeyedMutator<ApiResponse<User>>} {
	const { data, mutate, error } = useSWR<ApiResponse<User>>(`${API_URL}/user`)

	return {
		user: data?.payload ? data?.payload[0] : undefined,
		isLoading: !error && !data,
		user_mutate:mutate
	}
}
