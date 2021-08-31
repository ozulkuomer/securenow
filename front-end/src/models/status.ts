export class Status{
	text?:string = '';
	user_id?:number = -1;
}

export class StatusFactory{
	public static create_instance(status:Partial<Status>){
		const instance = new Status();
		instance.text = status.text ?? '';
		instance.user_id = status.user_id ?? -1;
		return instance
	}
}
