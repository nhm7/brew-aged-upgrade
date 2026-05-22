# typed: false
# frozen_string_literal: true

class AgedUpgrade < Formula
  desc "Upgrade Homebrew packages only after they have been outdated for N days"
  homepage "https://github.com/nhm7/homebrew-aged-upgrade"
  url "https://github.com/nhm7/homebrew-aged-upgrade/archive/refs/tags/v1.3.0.tar.gz"
  sha256 "0f13f50ea75f56d5b399fa5fb329a3ecedc4b055819365411397d44a0e64b832"

  head "https://github.com/nhm7/homebrew-aged-upgrade.git", branch: "main"
  license "MIT"

  depends_on :macos
  uses_from_macos "python3"

  def install
    libexec.install "libexec/brew-aged-upgrade", "libexec/brew-aged-upgrade-core.py", "libexec/Homebrew.png"
    bin.write_exec_script libexec/"brew-aged-upgrade"
  end

  def caveats
    <<~EOS
      The CLI is installed as `brew-aged-upgrade`, not `aged-upgrade`.

      To enable daily auto-upgrade:
        brew-aged-upgrade start
    EOS
  end

  test do
    output = shell_output("#{bin}/brew-aged-upgrade help")
    assert_match "start", output
    assert_match "stop", output
    assert_match "status", output
  end
end
