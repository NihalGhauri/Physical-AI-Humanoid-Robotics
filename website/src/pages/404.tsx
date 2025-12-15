import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

export default function NotFound() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Page Not Found | ${siteConfig.title}`}
      description="The requested page could not be found in the Physical AI & Humanoid Robotics textbook">
      <main className="container margin-vert--xl">
        <div className="row">
          <div className="col col--6 col--offset-3">
            <Heading as="h1" className="hero__title text--center">
              Page Not Found
            </Heading>
            <p className="text--center text--large margin-bottom--lg">
              We couldn't find the page you were looking for in the Physical AI & Humanoid Robotics textbook.
            </p>
            <div className="text--center margin-vert--lg">
              <Link className="button button--primary button--lg" to="/">
                Go to Homepage
              </Link>
              <Link className="button button--secondary button--lg margin-left--md" to="/docs/intro">
                Start Reading Textbook
              </Link>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}