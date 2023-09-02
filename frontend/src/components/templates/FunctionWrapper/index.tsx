import React from 'react'
import { Link, Outlet } from "react-router-dom";
import { Typography, Row, Col, Divider } from 'antd';
import { FunctionOutlined } from '@ant-design/icons';

const FunctionWrapper = () => {
    return (
        <Row>
            <Col span={24}>
                <Link to="/functions">
                    <Typography.Title level={3}>
                        <FunctionOutlined /> Functions
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

export default FunctionWrapper