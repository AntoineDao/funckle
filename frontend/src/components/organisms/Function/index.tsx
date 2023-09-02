import React from 'react'
import { Button, Card, Col, Row, Skeleton, Space, Typography } from 'antd';
import { CodeSandboxOutlined } from '@ant-design/icons'
import { Link, useParams, Route, Routes } from "react-router-dom";
import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { dracula } from 'react-syntax-highlighter/dist/esm/styles/prism'


import { useFunction } from '../../../hooks/useFunction'
import { useUser } from '../../../context/user'

import PageColumn from '../../templates/PageColumn';
import PackageList from '../../molecules/PackageList';
import Package from '../Package';

const SYNTAX_HIGHLIGHT = dracula

const Stream = () => {
    let { functionId } = useParams();

    const { func, functionVersions, loading, error, } = useFunction({ id: functionId as string })
    const { user } = useUser()

    return (
        <Row gutter={[16, 16]}>
            <Col span={12}>
                <PageColumn
                    header={[
                        <Typography.Text strong>Function</Typography.Text>
                    ]}
                >
                    <Row gutter={[16, 16]}>
                        <Col span={24}>
                            <Card bordered>
                                <Skeleton loading={loading} avatar paragraph={{ rows: 0 }}>
                                    <Card.Meta
                                        title={func?.slug}
                                        description={
                                            <Row justify='space-between' align='bottom'>
                                                <Col>
                                                    <Space>
                                                        <Typography.Text>{functionVersions.length} x</Typography.Text>
                                                        <CodeSandboxOutlined />
                                                    </Space>
                                                </Col>
                                            </Row>

                                        }
                                    />
                                </Skeleton>
                            </Card>
                        </Col>
                        <Col span={24}>
                            <Card bordered>
                                <Skeleton loading={loading} paragraph={{ rows: 5 }}>
                                    <ReactMarkdown
                                        children={func && func.readme ? func.readme : ''}
                                        components={{
                                            code({ node, inline, className, children, ...props }) {
                                                const match = /language-(\w+)/.exec(className || '')
                                                return !inline && match ? (
                                                    <SyntaxHighlighter
                                                        {...props}
                                                        children={String(children).replace(/\n$/, '')}
                                                        style={SYNTAX_HIGHLIGHT}
                                                        language={match[1]}
                                                        PreTag="div"
                                                    />
                                                ) : (
                                                    <code {...props} className={className}>
                                                        {children}
                                                    </code>
                                                )
                                            }
                                        }}
                                    />
                                </Skeleton>
                            </Card>
                        </Col>
                    </Row>
                </PageColumn>
            </Col>
            <Col span={12}>
                <Routes>
                    <Route index element={
                        <PageColumn
                            header={[
                                <Typography.Text strong>Packages</Typography.Text>,
                            ]}
                        >
                            <PackageList
                                functionId={functionId as string}
                                packages={functionVersions}
                            />
                        </PageColumn>
                    } />
                    <Route path=":versionId" element={
                        <PageColumn
                            header={[
                                <Typography.Text strong>Package</Typography.Text>,
                                <Link to={`/functions/${functionId}`}>
                                    <Button
                                        type="primary" size="small"
                                    >
                                        Back
                                    </Button>
                                </Link>
                            ]}
                        >
                            <Package functionId={functionId as string} />
                        </PageColumn>
                    } />
                </Routes>
            </Col>
        </Row>
    )
}

export default Stream