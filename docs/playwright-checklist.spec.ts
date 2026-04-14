import { test, expect, Page } from '@playwright/test'

/**
 * Camp7 docs Playwright 验收模板
 *
 * 用法：
 * 1. 安装 Playwright
 *    npm i -D @playwright/test
 *    npx playwright install
 *
 * 2. 设置站点地址
 *    export BASE_URL="http://localhost:3000"
 *    export DOCS_BASE_PATH="/docs"
 *
 * 3. 运行
 *    npx playwright test playwright-checklist.spec.ts
 *
 * 说明：
 * - 默认假设课程页面路径为:
 *   ${BASE_URL}${DOCS_BASE_PATH}/${slug}/readme
 *   ${BASE_URL}${DOCS_BASE_PATH}/${slug}/task
 * - 如果你们站点路由不同，只需要改 makeUrl()。
 */

const BASE_URL = process.env.BASE_URL || 'http://localhost:3000'
const DOCS_BASE_PATH = process.env.DOCS_BASE_PATH || '/docs'

type CourseCheck = {
  slug: string
  title: RegExp
  readmeMustContain: string[]
  readmeAtLeast?: { texts: string[]; min: number }
  taskMustContain: string[]
}

const courseChecks: CourseCheck[] = [
  {
    slug: 'introduction',
    title: /Camp7|课程|导学/i,
    readmeMustContain: ['你将做出什么'],
    readmeAtLeast: {
      texts: ['Claude Code', 'Skills', 'OpenClaw', 'LMDeploy', 'InternSVG'],
      min: 3,
    },
    taskMustContain: ['验收标准', '提交'],
  },
  {
    slug: 'claude-code',
    title: /Claude Code/i,
    readmeMustContain: ['Claude Code'],
    readmeAtLeast: {
      texts: ['npm install -g @anthropic-ai/claude-code', 'claude --version'],
      min: 1,
    },
    taskMustContain: ['验收标准', '截图'],
  },
  {
    slug: 'skills',
    title: /Skills/i,
    readmeMustContain: ['10 分钟跑通第一个 Skill'],
    readmeAtLeast: {
      texts: ['触发条件', '前置检查', '执行步骤', '质量标准'],
      min: 3,
    },
    taskMustContain: ['验收标准', '提交物'],
  },
  {
    slug: 'mcp',
    title: /MCP/i,
    readmeMustContain: ['Model Context Protocol', 'Tools'],
    taskMustContain: ['MCP', '验收标准'],
  },
  {
    slug: 'openclaw',
    title: /OpenClaw/i,
    readmeMustContain: ['Telegram', 'BotFather'],
    taskMustContain: ['Telegram', '验收标准'],
  },
  {
    slug: 'internsvg',
    title: /InternSVG/i,
    readmeMustContain: ['SVG'],
    readmeAtLeast: {
      texts: ['lmdeploy serve api_server', 'InternSVG-8B', '图片转 SVG'],
      min: 2,
    },
    taskMustContain: ['SVG', '提交'],
  },
  {
    slug: 'agent2agent',
    title: /Agent2Agent|A2A/i,
    readmeMustContain: ['MCP 与 A2A', 'Agent Card'],
    taskMustContain: ['A2A', '验收标准'],
  },
  {
    slug: 'intern-s1-pro',
    title: /Intern-S1-Pro/i,
    readmeMustContain: ['科学多模态大模型', 'OpenAI'],
    taskMustContain: ['API', '验收标准'],
  },
  {
    slug: 'lmdeploy',
    title: /LMDeploy/i,
    readmeMustContain: ['lmdeploy serve api_server', 'OpenAI'],
    taskMustContain: ['部署', '验收标准'],
  },
  {
    slug: 'internvl-u',
    title: /InternVL-U/i,
    readmeMustContain: ['A100', '华为昇腾 Atlas 800T A2'],
    readmeAtLeast: {
      texts: ['图像理解', '文生图', '图像编辑'],
      min: 2,
    },
    taskMustContain: ['验收标准', '图像'],
  },
]

function makeUrl(slug: string, pageName: 'readme' | 'task') {
  return `${BASE_URL}${DOCS_BASE_PATH}/${slug}/${pageName}`
}

async function assertPageHealthy(page: Page, expectedTitle: RegExp) {
  await expect(page).not.toHaveTitle(/404|Not Found/i)
  await expect(page.locator('h1')).toHaveCount(1)
  await expect(page.locator('h1')).toContainText(expectedTitle)
}

async function assertTextsPresent(page: Page, texts: string[]) {
  for (const text of texts) {
    await expect(page.getByText(text, { exact: false })).toBeVisible()
  }
}

async function assertAtLeastNTexts(page: Page, texts: string[], min: number) {
  let matched = 0
  for (const text of texts) {
    const locator = page.getByText(text, { exact: false }).first()
    if (await locator.isVisible().catch(() => false)) {
      matched += 1
    }
  }
  expect(
    matched,
    `expected at least ${min} text matches, got ${matched}: ${texts.join(', ')}`
  ).toBeGreaterThanOrEqual(min)
}

test.describe('Camp7 Docs Checklist', () => {
  for (const course of courseChecks) {
    test(`${course.slug} / readme`, async ({ page }) => {
      await page.goto(makeUrl(course.slug, 'readme'))
      await assertPageHealthy(page, course.title)
      await assertTextsPresent(page, course.readmeMustContain)
      if (course.readmeAtLeast) {
        await assertAtLeastNTexts(
          page,
          course.readmeAtLeast.texts,
          course.readmeAtLeast.min
        )
      }
    })

    test(`${course.slug} / task`, async ({ page }) => {
      await page.goto(makeUrl(course.slug, 'task'))
      await expect(page).not.toHaveTitle(/404|Not Found/i)
      await expect(page.locator('h1')).toHaveCount(1)
      await assertTextsPresent(page, course.taskMustContain)
    })
  }
})

test.describe('Camp7 Global Smoke Checks', () => {
  test('all readme pages have a single h1', async ({ page }) => {
    for (const course of courseChecks) {
      await page.goto(makeUrl(course.slug, 'readme'))
      await expect(page.locator('h1')).toHaveCount(1)
    }
  })

  test('all task pages contain at least 2 task-like keywords', async ({ page }) => {
    const keywords = ['任务', '提交', '验收标准']
    for (const course of courseChecks) {
      await page.goto(makeUrl(course.slug, 'task'))
      let matched = 0
      for (const keyword of keywords) {
        const locator = page.getByText(keyword, { exact: false }).first()
        if (await locator.isVisible().catch(() => false)) {
          matched += 1
        }
      }
      expect(
        matched,
        `${course.slug}/task should contain at least 2 of: ${keywords.join(', ')}`
      ).toBeGreaterThanOrEqual(2)
    }
  })
})
