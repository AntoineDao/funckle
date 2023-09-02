import React from 'react'
import { Link, Outlet } from "react-router-dom";
import { Typography, Row, Col, Breadcrumb, Divider } from 'antd';
import { DatabaseOutlined } from '@ant-design/icons';

const StreamWrapper = () => {
    return (
        <Row>
            <Col span={24}>
                <Link to="/streams">
                    <Typography.Title level={3}>
                        <DatabaseOutlined /> Streams
                    </Typography.Title>
                </Link>
                <Divider />
            </Col>
            <Col span={24}>
                <Outlet />
            </Col>
        </Row>
    )
}

export default StreamWrapper