export class User{
	_id?:number = -1;
	username?:string = '';
	email?:string = '';
}

export class UserFactory{
	public static create_instance(user:Partial<User>){
		const instance = new User();
		instance._id = user?._id ?? -1;
		instance.username = user.username ?? '';
		instance.email = user.email ?? '';
		return instance
	}
}
