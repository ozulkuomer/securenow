import { useUser } from "../../hooks/useUser";

interface PageBodyProps {
	children: JSX.Element | JSX.Element[];
}

export function PageBody({children}: PageBodyProps) {
	const {user} = useUser()

	return <main>
		<div className="content_box page_body">
			<aside>
				<div className="user_card">
					{
						user &&
						<div className={'avatar-container'}>
                            <img className={'avatar'} src={`https://i.pravatar.cc/128?u=${user.username}`} ></img>
                            <h1>{user.username}</h1>
						</div>
					}
				</div>
			</aside>

			<article>
				{children}
			</article>

			<aside>
				Right Component
			</aside>
		</div>
	</main>;
}
