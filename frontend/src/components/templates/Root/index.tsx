import React from 'react';
import { Typography, Layout, Menu, Card, Row, Col, theme } from 'antd';
import { Outlet, Link } from "react-router-dom";
import AuthButton from '../../molecules/AuthButton';

const { Header, Content, Footer } = Layout;

type Props = {
    children?: React.ReactNode
}


const Root = ({ children }: Props) => {
    const {
        token: { colorBgContainer },
    } = theme.useToken();

    return (
        <Layout className="layout">
            <Header>
                <Row justify='space-between' align='middle'>
                    <Col>
                        <Link to='/'>
                            <div className="demo-logo">
                                <Typography.Title level={3} style={{ margin: 0, color: 'white' }}>Funckle</Typography.Title>
                            </div>
                        </Link>
                    </Col>
                    <Col span={16}>
                        <Menu
                            theme="dark"
                            selectable={false}
                            mode="horizontal"
                            items={[{
                                key: 'functions',
                                label: (
                                    <Link to='/functions'>
                                        Functions
                                    </Link>
                                )
                            }, {
                                key: 'streams',
                                label: (
                                    <Link to='/streams'>
                                        Streams
                                    </Link>
                                )
                            }]}
                        />
                    </Col>
                    <Col>
                        <AuthButton />
                    </Col>
                </Row>


            </Header>
            <Content style={{ padding: '20px 20px', minHeight: '90vh' }}>
                {
                    children ? children : <Outlet />

                }
                {/* <Outlet /> */}
            </Content>
            <Footer style={{ textAlign: 'center' }}>Funckle Design</Footer>
        </Layout >
    );
};

export default Root;
