import { PageFooter } from "./components/page_footer";
import { PageHeader } from "./components/page_header";
import "./layout.css";
import { PageBody }   from "./components/page_body";

interface LayoutProps
{
	children: JSX.Element |  JSX.Element[];
}
export function Layout({children}:LayoutProps): JSX.Element {
	return (<div className="layout_root">
		<PageHeader/>
		<PageBody children={children} />
		<PageFooter/>
	</div>);

}
